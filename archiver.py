import json
import re
from archiver_packages.mega import mega_upload
from archiver_packages.htmls import ending
from archiver_packages.scrape_youtube import scrape_info
from archiver_packages.utilities.utilities import del_special_chars, convert_date_format, list_files_by_creation_date
from archiver_packages.utilities.selenium_utils import chrome_setup
from archiver_packages.utilities.youtube_utils import download_videos_with_info, get_youtube_links_from_playlist_and_channel, input_youtube_links
from archiver_packages.utilities.archiver_utils import remove_output_folder, chrome_version_exception

from archiver_packages.scrape_instagram import get_ig_post_with_info,add_comments


def modify_exctracted_info(video_publish_date:str,channel_keywords:list,channel_description:str,like_count:int|None,dislike_count:int|None,comment_count:int|None,video_title:str) -> tuple:

    # Modify date format
    video_publish_date = convert_date_format(video_publish_date)

    # Add hashtag to keyword tags
    channel_keywords = ['#'+i for i in channel_keywords]
    channel_keywords = ' '.join(channel_keywords)

    # Make description link-clickable
    channel_description = re.sub(r'http\S+', '<a href="' + "\\g<0>" + '">' + "\\g<0>" + '</a>', channel_description)

    # Add likes
    if like_count is not None:
        like_count = f'{like_count:,}'
    else:
        like_count = "LIKE"

    # Add dislikes
    if dislike_count is not None:
        dislike_count = f'{dislike_count:,}'
    else:
        dislike_count = "DISLIKE"

    # Add comments tag
    if comment_count is not None:
        comment_count = f"{comment_count:,} Comments"
    else:
        comment_count = "Comments are turned off."

    # Remove special characters to save file on windows
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

        # Scrape additional info
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
        print(f"HTML file created for {video_title}")

        input.close()
        output.close()


def parse_to_html_ig(yt_urls:list[str],mega_urls:list[str],info_list:list[dict],driver,delay:int,save_comments:bool):

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

        # Scrape additional info
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
        print(f"HTML file created for {video_title}")

        input.close()
        output.close()


def archiver(yt_urls:list,output_directory:str="downloaded"):

    # Load settings
    settings: dict = json.loads(open('settings.json', encoding="utf-8").read())

    save_comments = settings.get("youtube").get("save_comments")
    delay = settings.get("extra").get("delay")
    headless = settings.get("extra").get("headless")
    split_tabs = settings.get("extra").get("split_tabs")

    remove_output_folder(output_directory)

    print("\nDownloading videos...")

    # Extract yt urls from playlists and channels
    for yt_url in yt_urls:
        if "&list=" in yt_url:
            extracted_urls = get_youtube_links_from_playlist_and_channel(yt_url)
            yt_urls.remove(yt_url)
            yt_urls.extend(extracted_urls)
        elif "/@" in yt_url:
            extracted_urls = get_youtube_links_from_playlist_and_channel(yt_url)
            yt_urls.remove(yt_url)
            yt_urls.extend(extracted_urls)

    # Download yt videos and extract metadata
    info_list = download_videos_with_info(yt_urls,output_directory)

    # Load chromedriver
    try:
        driver = chrome_setup(
                            implicit_wait=delay+5,
                            profile="Default",
                            headless=headless,
                            split_tabs=split_tabs,
                            )
    except Exception as e:
        print(e)

        if "only supports Chrome version" in e:
            chrome_version_exception(e)

    # List downloaded videos
    files = list_files_by_creation_date(output_directory,except_extensions=[".json"])

    # Upload downloaded videos to Mega.io
    mega_urls = mega_upload(driver,delay,files)

    print("Files uploaded to Mega.")

    # Parse extracted metadata to html
    parse_to_html(yt_urls,mega_urls,info_list,driver,delay,save_comments)

    driver.quit()


def archiver_ig(ig_urls:list,output_directory:str="ig_data"):

    # Load settings
    settings: dict = json.loads(open('settings.json', encoding="utf-8").read())

    login = settings.get("mega_auth").get("login")
    password = settings.get("mega_auth").get("password")
    delay = settings.get("extra").get("delay")
    headless = settings.get("extra").get("headless")
    split_tabs = settings.get("extra").get("split_tabs")

    if login == "" or password == "":
        input("\nMega.io login credentials not found. Please enter them in settings.json")
        exit()

    # Load chromedriver
    try:
        driver = chrome_setup(
                            implicit_wait=delay+5,
                            profile="Default",
                            headless=headless,
                            split_tabs=split_tabs,
                            )
    except Exception as e:
        print(e)


    # Download ig post and extract data
    info_list = get_ig_post_with_info(driver,ig_urls,delay,output_directory)
    print(info_list)

    # # List downloaded videos
    # files = list_files_by_creation_date(output_directory,except_extensions=[".json"])

    # # Upload downloaded videos to Mega.io
    # mega_urls = mega_upload(driver,login,password,delay,files)

    # print("Files uploaded to Mega.")

    # # Parse extracted metadata to html
    # parse_to_html_ig(ig_urls,mega_urls,info_list,driver,delay,save_comments)

    driver.quit()



if __name__ == '__main__':

    # yt_urls = input_youtube_links()
    yt_urls = ["https://www.youtube.com/watch?v=xyCCb7yRgZ4"]
    archiver(yt_urls)

    # ig_urls = input_ig_links()
    # ig_urls = ["https://www.instagram.com/p/Cstf7qBSfiX/"]
    # archiver_ig(ig_urls)

    print("\nCompleted..")