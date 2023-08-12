import os
import json
import re
from modules.utilities.utilities import del_special_chars, convert_date_format, list_files_by_creation_date
from modules.utilities.selenium_utils import chrome_setup
from modules.mega import mega_upload
from modules.scrape_youtube import scrape_info,add_comments
from modules.htmls import ending
from modules.utilities.youtube_utils import download_videos_with_info, get_youtube_links_from_playlist, input_youtube_links



def remove_output_folder(output_directory:str):
    """
    Remove output folder to remove previously downloaded videos and 
    avoid link and downloaded video mismatch in parse_to_html() zip func
    """
    from shutil import rmtree

    if os.path.exists(output_directory):
        rmtree(output_directory)


def modify_exctracted_info(video_publish_date:str,channel_keywords:list,channel_description:str,like_count:int|None,dislike_count:int|None,comment_count:int|None,video_title:str) -> tuple:

    # modify date format
    video_publish_date = convert_date_format(video_publish_date)

    # add hashtag to keyword tags
    channel_keywords = ['#'+i for i in channel_keywords]
    channel_keywords = ' '.join(channel_keywords)

    # make description link-clickable
    channel_description = re.sub(r'http\S+', '<a href="' + "\\g<0>" + '">' + "\\g<0>" + '</a>', channel_description)

    # add likes
    if like_count is not None:
        like_count = f'{like_count:,}'
    else:
        like_count = "LIKE"

    # add dislikes
    if dislike_count is not None:
        dislike_count = f'{dislike_count:,}'
    else:
        dislike_count = "DISLIKE"

    # add comments tag
    if comment_count is not None:
        comment_count = f"{comment_count:,} Comments"
    else:
        comment_count = "Comments are turned off."

    # remove special characters to save file on windows
    video_title_filtered = del_special_chars(video_title)

    return (video_publish_date,channel_keywords,channel_description,like_count,dislike_count,comment_count,video_title_filtered)


def parse_to_html(yt_urls:list[str],mega_urls:list[str],info_list:list[dict],driver,delay:int,save_comments:bool):

    for (yt_url,mega_url,info) in zip(yt_urls,mega_urls,info_list):

        # Extract the relevant pieces of information
        video_title = info.get('title', None)
        video_views = info.get('view_count', None)
        channel_author = info.get('uploader', None)
        channel_url = info.get('uploader_url', "Channel URL not found")
        video_publish_date = info.get('upload_date', None)
        channel_keywords = info.get('tags', None)
        channel_description = info.get('description', None)
        subscribers = info.get('channel_follower_count', None)
        like_count = info.get('like_count', None)
        dislike_count = info.get('dislike_count', None)
        comment_count = info.get('comment_count', None)

        video_publish_date,channel_keywords,channel_description,like_count,dislike_count,comment_count,video_title_filtered = modify_exctracted_info(video_publish_date,channel_keywords,channel_description,like_count,dislike_count,comment_count,video_title)

        input = open("./yt_html_export/index.html", 'rt', encoding="utf8")
        output = open("./yt_html_export/"+video_title_filtered+".html", 'wt', encoding="utf8")

        #scrape additional info
        profile_image = scrape_info(driver,yt_url,delay)

        for line in input:
            output.write(line.replace('REPLACE_TITLE', video_title)
                            .replace('TITLE_URL', yt_url)
                            .replace('NUMBER_OF_VIEWS', f'{video_views:,}')
                            .replace('CHANNEL_AUTHOR', channel_author)
                            .replace('CHANNEL_URL', channel_url)
                            .replace('PUBLISH_DATE', f'{video_publish_date}')
                            .replace('CHANNEL_KEYWORDS', f'{channel_keywords}')
                            .replace('CHANNEL_DESCRIPTION', channel_description)
                            .replace('CHANNEL_SUBSCRIBERS', f'{subscribers:,}')
                            .replace('PROFILE_IMAGE_LINK', profile_image)
                            .replace('LIKE_COUNT', like_count)
                            .replace('DISLIKES_COUNT', dislike_count)
                            .replace('COMMENT_COUNT', f'{comment_count}')

                            .replace('VIDEO_SOURCE', f'{mega_url}'))

        if save_comments == True:
            add_comments(driver,profile_image,output,delay)

        output.write(ending.html_end)
        print(f"html created for {video_title}")

        input.close()
        output.close()


def archiver(yt_urls:list,output_directory:str="downloaded"):

    #load settings
    settings: dict = json.loads(open('settings.json', encoding="utf-8").read())

    login = settings.get("mega_auth").get("login")
    password = settings.get("mega_auth").get("password")
    save_comments = settings.get("youtube").get("save_comments")
    delay = settings.get("extra").get("delay")
    headless = settings.get("extra").get("headless")

    if login == "" or password == "":
        input("\nMega.io login credentials not found. Please enter them in settings.json")

    remove_output_folder(output_directory)

    print("\nDownloading videos...")

    #extract yt urls from playlists
    for yt_url in yt_urls:
        if "&list=" in yt_url:
            extracted_urls = get_youtube_links_from_playlist(yt_url)
            yt_urls.remove(yt_url)
            yt_urls.extend(extracted_urls)

    #download yt videos and extract metadata
    info_list = download_videos_with_info(yt_urls,output_directory)

    #load chromedriver
    driver = chrome_setup(
                        implicit_wait=delay+5,
                        headless=headless
                        )

    #list downloaded videos
    files = list_files_by_creation_date(output_directory,except_extensions=[".json"])

    #upload downloaded videos to Mega.io
    mega_urls = mega_upload(driver,login,password,delay,files)

    print("Files uploaded to Mega...")

    #parse extracted metadata to html
    parse_to_html(yt_urls,mega_urls,info_list,driver,delay,save_comments)

    driver.quit()



if __name__ == '__main__':

    yt_urls = input_youtube_links()
    #yt_urls = ["https://www.youtube.com/watch?v=-FShtfB--pQ","https://www.youtube.com/watch?v=LK6KVBnmWpU&list=PL8SZ21Qv2Fenl6Y7d0AqxJpKEf630g7HA&index=1"]

    archiver(yt_urls)

    print("\nCompleted..")