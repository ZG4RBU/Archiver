import os


def clear():
    os.system('cls' if os.name=='nt' else 'clear')


def input_youtube_links() -> list[str]:

    yt_links = []
    try:
        while True:
            print("\nNOTE:")
            print("Add YouTube Videos/Playlists one by one. Finally type 'S/s' to start")
            link = input("\n >> Add YouTube link: ")

            if link.lower()=='s':
                break
            if link not in yt_links: #avoid duplicates
                yt_links.append(link)

            #print Full list
            clear()
            print("Links Added\t")
            for yt_link in yt_links:
                print(yt_link)
    except:
        print(f"Make sure, the YouTube links are in a correct format.")

    return yt_links