import re


def extract_emoji_unicode(url:str) -> str|None:
    # Define a regular expression pattern to match the emoji unicode
    pattern = r"emoji_(\w+)\.png"

    # Use the findall function to search for all occurrences of the pattern in the URL
    matches = re.findall(pattern, url)

    # If there are matches, return the first match found
    if matches:
        return matches[0]
    else:
        return None


def convert_to_unicode(emoji_unicode):
    # Strip 'u' and convert to uppercase
    emoji_unicode = emoji_unicode.strip('u').upper()
    # Pad with zeros to make sure it's 8 characters long
    emoji_unicode = emoji_unicode.zfill(8)
    # Prefix with 'U'
    emoji_unicode = '\\U' + emoji_unicode
    return emoji_unicode

def unicode_to_emoji(text):
    # Regular expression to find Unicode characters
    unicode_pattern = re.compile(r'\\U[0-9a-fA-F]{8}')

    # Replace Unicode characters with emojis
    def replace(match):
        char = match.group(0)
        emoji = chr(int(char[2:], 16))
        return emoji

    return unicode_pattern.sub(replace, text)


def convert_youtube_emoji_url_to_emoji(url:str) -> str:

    url_unicode = extract_emoji_unicode(url)
    unicode_code = convert_to_unicode(url_unicode)
    emoji_text = unicode_to_emoji(unicode_code)
    return emoji_text


if __name__ == '__main__':

    url="https://www.youtube.com/s/gaming/emoji/7ff574f2/emoji_u1f525.png"

    convert_youtube_emoji_url_to_emoji(url)