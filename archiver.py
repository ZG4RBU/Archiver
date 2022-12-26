import os
import re
from shutil import rmtree
from colorama import init, Fore, Style
init(autoreset=True)
from configparser import ConfigParser
from pytube import YouTube,Playlist,Channel
from mega import mega_upload
from scrape_youtube import scrape,add_comments
from htmls import ending
#rashvebi

config = ConfigParser()
config.read('Settings.ini')

login = config.get('mega_auth', 'login')
password = config.get('mega_auth', 'password')
save_comments = config.get('youtube', 'save_comments')
delay = config.getint('delay', 'seconds')
headless = config.get('extra', 'headless')


def on_complete(stream, filepath):
	print(Fore.GREEN + Style.BRIGHT + 'download complete')
	print(filepath)

def on_progress(stream, chunk, bytes_remaining):
	progress_string = f'{round(100 - (bytes_remaining / stream.filesize * 100),2)}%'
	print(progress_string)

def clear():
    os.system('cls' if os.name=='nt' else 'clear')



def input_youtube_links() -> list:

    links_list = []
    try:
        while True:
            print("\nNOTE:")
            print("Add your YouTube links here. finally type 'S/s' to start")
            link = input("\n >> Add a link: ")
            
            if link.lower()=='s':
                break
            elif link in links_list: #avoid duplicates
                pass
            elif any(x in link for x in ['/channel/', '/c/']):
                links_list.extend(Channel(link))
            elif 'playlist?' in link:
                links_list.extend(Playlist(link))
            else:
                links_list.append(link)

            #print Full list
            clear()
            print("Author\t Title\t  Link\t")
            for link in links_list:
                print(YouTube(link).author + '\t '+ YouTube(link).title + '\t ' + link)
    except:
        print(f"Make sure, the YouTube links are in a correct format.")
    
    return links_list


def download_yt_videos(yt_links:list):
    
    path = "upload"
    
    #remove folder to avoid link and video mismatch in line #102 zip func
    if os.path.exists(path):
        rmtree(path)

    print("\ndownloading...")

    for yt_link in yt_links:
        video_object = YouTube(yt_link,
                                on_complete_callback = on_complete,
                                on_progress_callback = on_progress)

        video_object.streams.get_highest_resolution().download(path)



def parse_to_html(yt_links:list,mega_links:list):

    for (yt_link, mega_link) in zip(yt_links, mega_links):

        video_object = YouTube(yt_link)

        #make description link-clickable
        description = re.sub(r'http\S+', '<a href="' + "\\g<0>" + '">' + "\\g<0>" + '</a>', video_object.description)
        #remove hour/min from publish date
        publish_date = str(video_object.publish_date)[:-8]
        #add hashtag to keyword tags
        keywords = ['#'+i for i in video_object.keywords]
        keywords = ' '.join(keywords)


        #remove special chars in video title to save file locally
        special_chars = ["/","\\",":","*","?",'"',"<",">","|"]
        for char in special_chars:
            if char in video_object.title:
                video_object.title=video_object.title.replace(char, "")

        input = open("./yt_html_export/index.html", 'rt', encoding="utf8")
        output = open("./yt_html_export/"+video_object.title+".html", 'wt', encoding="utf8")

        #scrape more info
        subscribers,like_count,profile_image,comments_count = scrape(yt_link,delay,headless)

        for line in input:
            output.write(line.replace('REPLACE_TITLE', f'{video_object.title}')
                            .replace('TITLE_URL', f'{yt_link}')
                            .replace('NUMBER_OF_VIEWS', f'{video_object.views:,}')
                            .replace('CHANNEL_AUTHOR', f'{video_object.author}')
                            .replace('CHANNEL_URL', f'{video_object.channel_url}')
                            .replace('PUBLISH_DATE', publish_date)
                            .replace('CHANNEL_KEYWORDS', keywords)
                            .replace('CHANNEL_DESCRIPTION', description)

                            #scrape()
                            .replace('CHANNEL_SUBSCRIBERS', f'{subscribers}')
                            .replace('PROFILE_IMAGE_LINK', f'{profile_image}')
                            .replace('LIKE_COUNT', f'{like_count}')
                            .replace('COMMENTS_COUNT', f'{comments_count}')

                            .replace('VIDEO_SOURCE', f'{mega_link}'))

        if save_comments == 'True':
            add_comments(yt_link,profile_image,output,delay,headless)

        output.write(ending.html_end)

        print(Fore.GREEN + Style.BRIGHT + f'html created for {video_object.title}')

        input.close()
        output.close()


if __name__ == '__main__':
    
    #download yt videos
    yt_links = input_youtube_links()
    download_yt_videos(yt_links)
    
    #upload to mega
    mega_links = mega_upload(login,password,delay,headless)
    print(Fore.GREEN + Style.BRIGHT + 'files uploaded to mega...')
    
    parse_to_html(yt_links,mega_links)

    input(Fore.GREEN + Style.BRIGHT + '\nfinished ...')



