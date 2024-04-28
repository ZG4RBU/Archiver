import json
import re
from archiver_packages.mega import mega_upload
from archiver_packages.youtube_html_elements import ending
from archiver_packages.youtube.extract_info import scrape_info
from archiver_packages.youtube.add_comments import add_comments
from archiver_packages.utilities.utilities import convert_date_format 
from archiver_packages.utilities.file_utils import move_file, create_directory, copy_file_or_directory, list_files_by_creation_date
from archiver_packages.utilities.selenium_utils import chrome_setup
from archiver_packages.youtube.download_video import download_videos_with_info, get_youtube_links_from_playlist_and_channel, input_youtube_links
from archiver_packages.utilities.archiver_utils import rename_directory_with_timestamp, chrome_version_exception
import os



def extract_filename_without_extension(file_path):
    filename_with_extension = os.path.basename(file_path)
    filename_without_extension, _ = os.path.splitext(filename_with_extension)
    return filename_without_extension


def modify_exctracted_info(video_publish_date:str,channel_keywords:list,channel_description:str,like_count:int|None,dislike_count:int|None,comment_count:int|None) -> tuple:

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

    return (video_publish_date,channel_keywords,channel_description,like_count,dislike_count,comment_count)


def get_html_output_dir(video_id:str) -> str:

    root_directory = 'downloaded'

    for dir in os.listdir(root_directory):
        if video_id in dir:
            return dir


def parse_to_html(yt_urls:list[str],mega_urls:list[str],info_list:list[dict],driver,delay:int,save_comments:bool,max_comments:int):

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

        video_publish_date,channel_keywords,channel_description,like_count,dislike_count,comment_count = modify_exctracted_info(video_publish_date,channel_keywords,channel_description,like_count,dislike_count,comment_count)

        html_output_dir = get_html_output_dir(info.get("id"))

        input = open("./archiver_packages/youtube_html/index.html", 'rt', encoding="utf8")
        output = open(f"./downloaded/{html_output_dir}/{html_output_dir}.html", 'wt', encoding="utf8")

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
            add_comments(driver,profile_image,output,delay,max_comments)

        output.write(ending.html_end)
        print(f"HTML file created for {video_title}")

        input.close()
        output.close()

        # Copy assets folder and style.css to html output dir
        copy_file_or_directory(
            "archiver_packages/youtube_html/assets",
            f"downloaded/{html_output_dir}"
        )
        copy_file_or_directory(
            "archiver_packages/youtube_html/style.css",
            f"downloaded/{html_output_dir}"
        )


def archiver(yt_urls:list,output_directory:str="downloaded"):

    # Load settings
    settings: dict = json.loads(open('settings.json', encoding="utf-8").read())

    save_comments = settings.get("youtube").get("save_comments")
    max_comments = settings.get("youtube").get("max_comments")
    delay = settings.get("extra").get("delay")
    headless = settings.get("extra").get("headless")
    split_tabs = settings.get("extra").get("split_tabs")

    rename_directory_with_timestamp(output_directory)

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

    # List downloaded videos
    files = list_files_by_creation_date(output_directory,except_extensions=[".json"])
    files_updated = []

    # Move downloaded videos and info files to output folder
    for file in files:
        filename_without_extension = extract_filename_without_extension(file)
        html_dir = f"downloaded/{filename_without_extension}"
        create_directory(html_dir)
        move_file(file, html_dir)

        file_new_dir = f"downloaded/{html_dir}/{filename_without_extension}.mp4"
        files_updated.append(file_new_dir)

        # Move json files to html folder
        for file in os.listdir(output_directory):
            file = f"{output_directory}/{file}"
            if filename_without_extension in file and file.endswith(".json"):
                move_file(file, html_dir)

    files = files_updated

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

    # Upload downloaded videos to Mega.io
    mega_urls = mega_upload(driver,delay,files)

    print("Files uploaded to Mega.")

    # Parse extracted metadata to html
    parse_to_html(yt_urls,mega_urls,info_list,driver,delay,save_comments,max_comments)

    driver.quit()


if __name__ == '__main__':
    # yt_urls = input_youtube_links()
    yt_urls = ["https://www.youtube.com/watch?v=xyCCb7yRgZ4"]
    archiver(yt_urls)

    print("\nCompleted..")