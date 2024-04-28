import os
from datetime import datetime



def clear():
    os.system('cls' if os.name=='nt' else 'clear')


def convert_date_format(input_date:str) -> str:

    # Parse the input date in the format "YYYYMMDD"
    parsed_date = datetime.strptime(input_date, "%Y%m%d")

    # Format the parsed date to "day Month Year" (e.g., "5 May 2022")
    formatted_date = parsed_date.strftime("%d %B %Y")

    return formatted_date