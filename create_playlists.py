import json
from pathlib import Path

from get_bible_book_metadata import get_bible_book_metadata

bible_audio_path = "/storage/emulated/0/Music/TBAudio/"

YEAR = 2021
SCRIPT_DIR = Path(__file__).resolve().parent
YEAR_DIR = SCRIPT_DIR / str(YEAR)


def get_folder(name, data):

    testament = data["ot_nt"]
    book_num = data['book_num']
    if testament == "nt":
        # book_num for Matthew = "01", for Mark = "02", etc.
        book_num = f"{int(book_num) - 39:02}"
    # "1 Kings" -> "1-Kings", ..., "3 John" -> "3-John"
    book_name = name if name[1] != " " else f"{name[0]}-{name[2:]}"
    # Remove blanks from "Song of Solomon"
    book_name = book_name.replace(" ", "")
    subfolder = f"{book_num}_{book_name}".lower()

    return f"{testament}/{subfolder}"


def get_book_path(book_name, book_data):
    return f"{bible_audio_path}{get_folder(book_name, book_data)}"


# for book_name, book_data in get_bible_book_metadata().items():
#     print(get_book_path(book_name, book_data))

with open(YEAR_DIR / "bible_readings.json", "r") as json_file:
    bible_readings = json.load(json_file)

for date, daily_readings in bible_readings.items():
    print(date)
    for reading in daily_readings:
        book = reading[0]
        passages = reading[1]
        if (not isinstance(passages, int)) and passages.find(",") != -1:
            for passage in passages.split(", "):
                print(f"\t{book} {passage}")
        else:
            print(f"\t{book} {passages}")
