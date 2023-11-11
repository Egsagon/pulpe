<img src="https://raw.githubusercontent.com/Egsagon/pulpe/master/client/logo.svg?token=GHSAT0AAAAAACG2AQ6CGOYALWI5JI664PAOZKPOWDA"
       align="right"
       width="200px">

# PULPE

Pulpe is a simple file extractor and web UI for Outplayed. It supports searching, item reload and infinite scrolling.
It is specifically oriented towards Valorant replays at the moment, but aims to be polyvant for any game in the future.

It focuses on an ad-less, clean and minimal UI to watch your replays.
It also exports and renames Outplayed recordings so you don't have to deal with their weird names.

<br clear="right">

## Installation

1. Clone this repository: `git clone https://github.com/Egsagon`
2. Start the `pulpe.bat` file. While it remains opened, the server is running.
3. Open (this URL)[http://127.0.0.1:5000/] in your prefered browser.

## Manual interactions

If you have already extracted some videos and you want to view them with Pulpe, simply copy them into the `pulpe/data` folder.
Make sure all the filenames have the folowing format: `agentname-killcount-anyotherinformation.mp4`. Otherwise, the client
won't be able to display them.

## License

Pulpe uses the `GPL-v3` license. See the `LICENSE` file for more information.
