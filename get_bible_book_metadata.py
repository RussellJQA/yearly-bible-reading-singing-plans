import csv
import json
import os
from pathlib import Path
"""
columns in bible_book_metadata.csv:
0: book_num = 0-padded book number (01..66) in the Bible
1: hebrew_ot_num = 0-padded book number (01..39) in Hebrew OT order
    derived from
        https://www.bible-history.com/biblestudy/charts/
            old-testament-books-hebrew-order.html
2: book_name [used as book's key in bible_book_metadata dict]
3: cambridge_abbrev
4: logos_most_common_abbrev = Most Common of Bible Book Abbreviations
    from https://www.logos.com/bible-book-abbreviations
5: num_chapters
6: ot_nt
7: author
8: classifications
"""


def get_bible_book_metadata():

    script_dir = Path(__file__).resolve().parent
    csv_fn = script_dir / "source" / "bible_book_metadata.csv"
    json_fn = "bible_book_metadata.json"

    bible_book_metadata = {}

    rebuild_json = True
    if Path(json_fn).exists():
        csv_fn_last_modified = os.stat(csv_fn).st_mtime
        json_fn_last_modified = os.stat(json_fn).st_mtime
        rebuild_json = csv_fn_last_modified > json_fn_last_modified

    if rebuild_json:
        with open(csv_fn, newline="") as csv_file:
            headers = ""
            for book_index, book_row in enumerate(csv.reader(csv_file)):
                if book_index:
                    book_data = {}
                    for column_index, column in enumerate(book_row):
                        book_data[headers[column_index]] = column
                    book_name = book_data.pop("book_name")
                    bible_book_metadata[book_name] = book_data
                else:
                    headers = book_row

        with open(json_fn, "w") as json_file:
            json.dump(bible_book_metadata, json_file, indent=4)
    else:
        with open(json_fn, "r") as json_file:
            bible_book_metadata = json.load(json_file)

    return bible_book_metadata


if __name__ == "__main__":
    get_bible_book_metadata()
