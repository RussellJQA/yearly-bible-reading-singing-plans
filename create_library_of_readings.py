import csv
import json
from pathlib import Path

from get_bible_book_metadata import get_bible_book_metadata


def create_chapters_json(chapters_dict, json_filepath):
    chapters = {}
    readings = 0
    for book_name, book_data in chapters_dict.items():
        for chapter in range(1, int(book_data["num_chapters"]) + 1):
            readings += 1
            chapters[readings] = [book_name, chapter]
    with open(json_filepath, "w") as json_file:
        json.dump(chapters, json_file, indent=4)


def create_library_of_readings(bible_book_metadata):

    script_dir = Path(__file__).resolve().parent
    source_dir = script_dir / "source"
    library_dir = script_dir / "library"

    # Book lists for various readings
    ot = {}  # NT
    solomon = {}  # Writings of "Solomon" (Proverbs, Ecclesiastes, SoS)
    ot_wo_psalms = {}  # OT w/o Psalms
    ot_wo_das_hebrew_order = {}  # Hebrew-ordered OT w/o David & Solomon
    nt = {}  # NT

    ot_wo_das = {}  # OT without writings of David and Solomon
    hebrew_ot_order = {}
    for book_name, book_data in bible_book_metadata.items():
        if book_data["ot_nt"] == "ot":
            ot[book_name] = book_data
            if book_data["author"] == "Solomon":
                solomon[book_name] = book_data
                ot_wo_psalms[book_name] = book_data
            elif book_data["author"] != "David":  # book_name not Psalms
                ot_wo_psalms[book_name] = book_data
                ot_wo_das[book_name] = book_data
                hebrew_ot_order[book_data["hebrew_ot_num"]] = book_name
        else:
            nt[book_name] = book_data

    for hebrew_ot_num in sorted(hebrew_ot_order.keys()):
        book_name = hebrew_ot_order[hebrew_ot_num]
        ot_wo_das_hebrew_order[book_name] = bible_book_metadata[book_name]

    # The following file isn't used for the 2021 or 2022 plans
    create_chapters_json(ot, library_dir / "ot_chapters.json")

    create_chapters_json(nt, library_dir / "nt_chapters.json")

    # The following file is used by the 2022 plan
    create_chapters_json(ot_wo_psalms, library_dir / "ot_wo_psalms.json")

    # The following 2 files are used by the 2021 plan
    create_chapters_json(solomon, library_dir / "solomon_chapters.json")
    create_chapters_json(
        ot_wo_das_hebrew_order, library_dir / "ot_wo_das_ho_readings.json"
    )

    readings_per_chapter = {}
    fpcr_psalm_readings = {}
    with open(source_dir / "fpcr_psalm_readings.csv", newline="") as csv_file:
        for reading_count, reading in enumerate(csv.reader(csv_file), 1):
            chapter_and_verses = reading[0]
            fpcr_psalm_readings[reading_count] = ["Psalms", chapter_and_verses]
            chapter = chapter_and_verses[: chapter_and_verses.find(":")]
            readings_per_chapter[chapter] = readings_per_chapter.get(chapter, 0) + 1

    # For any reading of an entire Psalm (chapter), eliminate the verse numbers
    for reading in fpcr_psalm_readings.values():
        chapter_and_verses = reading[1]
        chapter = chapter_and_verses[: chapter_and_verses.find(":")]
        if readings_per_chapter[chapter] == 1:
            reading[1] = chapter

    with open(library_dir / "fpcr_psalm_selections.json", "w") as json_file:
        json.dump(fpcr_psalm_readings, json_file, indent=4)


if __name__ == "__main__":
    create_library_of_readings(get_bible_book_metadata())
