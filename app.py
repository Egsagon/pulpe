import os
import json
import glob
import flask
import shutil
import hashlib

OUTPUT = './data'
PAGE_LENGTH = 8

AGENTS = {
    'aggrobot':     'Gekko'   ,
    'bountyhunter': 'Fade'    ,
    'breach':       'Breach'  ,
    'cable':        'Deadlock',
    'clay':         'Raze'    ,
    'deadeye':      'Chamber' ,
    'grenadier':    'KAYO'    ,
    'guide':        'Skye'    ,
    'gumshoe':      'Cypher'  ,
    'hunter':       'Sova'    ,
    'killjoy':      'KillJoy' ,
    'mage':         'Harbor'  ,
    'pandemic':     'Viper'   ,
    'phoenix':      'Phoenix' ,
    'rift':         'Astra'   ,
    'sarge':        'Brim'    ,
    'sequoia':      'Iso'     ,
    'sprinter':     'Neon'    ,
    'stealth':      'Yoru'    ,
    'thorne':       'Sage'    ,
    'vampire':      'Reyna'   ,
    'wraith':       'Omen'    ,
    'wushu':        'Jett'
}

app = flask.Flask(__name__, static_folder = 'client')

def parse():
    '''
    Get and parse Outplayed data.
    '''
    
    # Get the data path
    results = glob.glob(os.getenv('APPDATA') + '/Overwolf/*/backup.json')    
    assert len(results) == 1, 'Failed to fetch Outplayed data'
    
    # Parse file
    with open(results[0], encoding = 'utf-8') as file:
        entries = json.load(file)
    
    # Extract data
    for uuid, play in entries.items():
        
        if not uuid.startswith('MATCH') or uuid.startswith('MATCH_ACTIONS'):
            continue
        
        play = json.loads(json.loads(play))
        agent = AGENTS.get(play['info'].get('agentKey', '')[:-5].lower())
        if not agent: continue
        
        for media in play['medias']:
            
            path = os.path.normpath(media['path']).replace('\\', '/')
            if not path or not os.path.exists(path): continue
            
            kills = len([i for i in media['events'] if i['type'] == 'kill'])
            if kills > 7: continue # TODO
            
            yield {'path': path, 'kills': kills, 'agent': agent}

@app.route('/')
def route():
    '''
    Return the home page.
    '''
    
    return flask.send_file('client/index.html')

@app.route('/get/<name>')
def get(name: str):
    '''
    Get a specific video.
    '''
    
    return flask.send_from_directory(OUTPUT, name)

@app.route('/open')
def open_():
    '''
    Open ressource folder.
    '''
    
    path = os.path.normpath(OUTPUT)
    os.popen(f'explorer {path}')
    
    return 'ok'

@app.route('/search')
def search():
    '''
    Get matching results.
    Used on client start to get first page.
    '''
    
    query = flask.request.args.get('query', '')
    page = int(flask.request.args.get('page', 0)) * PAGE_LENGTH
    
    return [os.path.basename(path)
            for path in sorted(glob.glob(f'{OUTPUT}/*{query}*.mp4'),
                               key = os.path.getmtime)][page:page + PAGE_LENGTH]

@app.route('/refresh')
def refresh():
    '''
    Refresh data from Outplayed.
    '''
    
    try:
        items = list(parse())
        
        for item in items:
            
            path = item['path']
            
            with open(path, 'rb') as file:
                md5 = hashlib.md5(file.read()).hexdigest()
            
            dest = f'{OUTPUT}/{item["agent"].lower()}-{item["kills"]}k-{md5}.mp4'
            
            if os.path.exists(dest):
                print('Skipping already copied: ', dest)
                continue
            
            # Copy
            print(f'Copying {path} to {dest}')
            shutil.copy(item['path'], dest)
    
        return 'ok'

    except Exception as err:
        return flask.jsonify({'error': repr(err)})


if __name__ == '__main__':
    app.run(debug = True)

# EOF