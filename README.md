# Archiver
Save youtube videos offline as html files.  
Download an [example](https://mega.nz/file/pTNiwSxT#9wcvhHxYaoEhYMyMv9Ny5honlbdBqppOekpQ0zdDoNs) 

![archiver_thumbnail](https://i.imgur.com/4PjU7B2.png)

## Use Cases
- download youtube videos that may get deleted later, in my case its music videos.
- Archiver can also be used as an OSINT tool to visualize gathered info better.

## How it works
Archiver is heavily dependent on selenium and pytube modules. Firstly, the youtube videos are downloaded locally and uploaded on mega.nz. After the downloads finish, mega.nz link and youtube link content are parsed to html blocks, from which the html file is built.

## Prerequisites
1. Python 3.6+
2. Google Chrome
3. mega.nz account

## Setup
1. download code
2. run requirements.cmd
3. go to `chrome://settings/help` in Chrome and update browser to the latest version
4. modify "Settings.ini" file

## Settings
`mega_auth` > enter your mega account login info

`youtube > save_comments` > enter True/false

`delay` > delay per action

`extra > headless` > run chrome as background process. enter True/false

## Usage
run `start.cmd` or run the command in terminal
```
python3 archiver.py
``` 
- html output will be saved in `yt_html_export` folder.
- when moving html file outside the folder make sure to copy css and assets folder as well.

## Task list
- [ ] Add delight to the experience when all tasks are complete

## Credits
thanks @virag-ky for https://github.com/virag-ky/Youtube-Clone for html/css  
For help contact @`zg4rbu#8684` (Discord)
