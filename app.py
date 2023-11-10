import os
import glob
import flask

OUTPUT = './data'
PAGE_LENGTH = 8

app = flask.Flask(__name__, static_folder = 'client')

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
    
    return [
        os.path.basename(path)
        for path in glob.glob(f'{OUTPUT}/*{query}*.mp4')
    ][page:page + PAGE_LENGTH]

@app.route('/refresh')
def refresh():
    '''
    Refresh data from Outplayed.
    '''
    
    return 'Not implemented'


if __name__ == '__main__':
    app.run(debug = True)

# EOF