# Archiver    
Save YouTube videos offline, complete with metadata, in an HTML interface that replicates the YouTube experience.  
Download an [example output](https://mega.nz/file/8ARy3QBQ#P93hzdTLX4Zxa6OhfHV6u8C8ZR8bQG6C6Yn5ChkLnGw)

![archiver_thumbnail](https://i.imgur.com/4PjU7B2.png)

## Use Cases
- Download YouTube videos that may be deleted later.
- Archiver can also be used as an OSINT tool to better visualize gathered information.

## How it Works
Archiver heavily depends on the selenium and yt-dlp modules. Initially, the YouTube videos are downloaded locally and then uploaded to mega.io. Once the downloads are completed, the mega.io video embed link and YouTube video content are placed into HTML blocks, which are then used to build the HTML file.

## Prerequisites
1. Python 3.10+
2. Latest version of Google Chrome
3. Mega.io account

## Setup
1. Download the code directly or clone the repository using `git clone https://github.com/ZG4RBU/Archiver.git`.
2. Install the necessary modules listed in `requirements.txt` by running `pip install -r requirements.txt`. Alternatively, on Windows, you can simply run the `requirements.cmd` script.
3. Make sure you have the latest version of Google Chrome installed. This is required for the Selenium ChromeDriver component.
4. Log in to mega.nz on your default Google Chrome profile. Additionally, it is required that the mega.nz file display is set to List view instead of Thumbnail view.
5. Customize the `settings.json` file according to your preferences.

## Settings
`youtube > save_comments` > Enter true/false.

`extra > delay` > Delay per action.

`extra > headless` > Run chrome as background process. Enter true/false.

NOTE:
When setting the headless option to true, it's essential to keep the Chrome browser window open and avoid minimizing it. If you need to multitask, it's recommended to resize the browser window to one half of the screen for a seamless working experience.


## Usage
To start the code, execute the following command:
```
python3 archiver.py
```
If you're on Windows, you can use the `start.cmd` script for an easy launch.
- The HTML output is saved in the `yt_html_export` folder.
- When moving the HTML file outside the folder, make sure to also copy the `css` file and `assets` folder.

## To-Do List
- [ ] Implement support for downloading content from Instagram and TikTok
- [ ] Enhance user interface for a more intuitive and user-friendly experience.
- [ ] Explore the possibility of adding support for additional video platforms.
- [ ] Enhance the writing and documentation for improved clarity.

## Credits
big thanks to @virag-ky for [this](https://github.com/virag-ky/Youtube-Clone) awesome html/css  

For help contact @`zg4rbu#8684` (Discord)
