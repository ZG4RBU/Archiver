# Archiver
Save youtube videos offline as html file. Archiver can also be used as OSINT tool to better visualize saved contents

![This is an image](https://myoctocat.com/assets/images/base-octocat.svg)

## prerequisites
1. Python 3.6+
2. Google Chrome
3. mega.nz account

## Setup
1. download code
2. run requirements.cmd
3. go to [chrome://settings/help](chrome://settings/help) in chrome and update browser to the latest version
4. modify "Settings.ini" file

## Settings
`mega_auth` > enter your mega account login info

`youtube > save_comments` > enter True/false

`delay` > delay per action

`extra > headless` > run chrome as background process. enter True/false

## Usage
run start.cmd or run ```python archiver.py``` in terminal. 
html output will be saved in `yt_html_export` folder.
when moving html file outside the folder make sure to copy css and assets folder as well.

## Task list
- [ ] Add delight to the experience when all tasks are complete
