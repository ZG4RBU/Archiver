# Archiver    
Save YouTube videos offline, complete with metadata, in an HTML interface that replicates the YouTube experience. 
Download an [example output](https://mega.nz/file/sbUGzCDS#HC_x1rCr22RRaNQSQWfZXh7Jd8BBIVJhSWycEgRvRAo)

![archiver_thumbnail](https://i.imgur.com/4PjU7B2.png)

## Use Cases
- Download YouTube videos that may be deleted later, in my case, it's music videos.
- Archiver can also be used as an OSINT tool to better visualize gathered information.

## How it Works
Archiver heavily depends on the selenium and yt-dlp modules. Initially, the YouTube videos are downloaded locally and then uploaded to mega.io. Once the downloads are completed, the mega.io video embed link and YouTube video content are placed into HTML blocks, which are then used to build the HTML file.

## Prerequisites
1. Python 3.6+
2. Google Chrome
3. Mega.io account

## Setup
1. Download code
2. Run requirements.cmd
3. Modify `settings.json` file

## Settings
`mega_auth` > Enter your mega account login info

`youtube > save_comments` > Enter true/false

`extra > delay` > Delay per action

`extra > headless` > Run chrome as background process. Enter True/false

## Usage
Run `start.cmd` or run the command in terminal
```
python3 archiver.py
``` 
- The HTML output is saved in the `yt_html_export` folder.
- When moving the HTML file outside the folder, make sure to also copy the `css` file and `assets` folder.

## Credits
thanks @virag-ky for [this](https://github.com/virag-ky/Youtube-Clone) awesome html/css  

For help contact @`zg4rbu#8684` (Discord)
