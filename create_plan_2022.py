import datetime
import json
from pathlib import Path
import re

from create_rtf_and_pdf import add_to_bible_readings
from create_rtf_and_pdf import create_rtf_and_pdf
from get_bible_book_metadata import get_bible_book_metadata
from create_library_of_readings import create_library_of_readings
from create_bible_audio_playlist import create_bible_audio_playlist

YEAR = 2022
THIS_YEAR_START = datetime.date(YEAR, 1, 1)
DAYS_IN_YEAR = (datetime.date(YEAR + 1, 1, 1) - THIS_YEAR_START).days
SCRIPT_DIR = Path(__file__).resolve().parent
LIBRARY_DIR = SCRIPT_DIR / "library"
YEAR_DIR = SCRIPT_DIR / str(YEAR)


def get_ot_wo_psalms(year):

    ot_wo_psalms = {}

    with open(LIBRARY_DIR / "ot_wo_psalms.json", "r") as json_file:
        selections = json.load(json_file)

    reading_num = 1

    for days in range(DAYS_IN_YEAR):

        date = THIS_YEAR_START + datetime.timedelta(days=days)
        day_of_week = date.strftime("%a")[:2].replace("Su", "LD")
        days_readings = []

        if (reading := selections.get(str(reading_num), "")) != "":

            # Add 1st of daily OT w/o Psalms readings

            days_readings.append(reading)
            reading_num += 1

            if (reading := selections.get(str(reading_num), "")) != "":

                # Add 2nd of daily OT w/o Psalms readings

                previous_book = days_readings[-1][0]
                current_book = reading[0]
                # If next reading is in same book, then merge the readings
                if previous_book == current_book:
                    merged_chapters = f"{days_readings[-1][1]}-{reading[1]}"
                    days_readings[-1][1] = merged_chapters
                else:
                    days_readings.append(reading)
                reading_num += 1

                if (
                    day_of_week == "Sa"
                    and date <= THIS_YEAR_START + datetime.timedelta(days=48 * 7)
                    and (reading := selections.get(str(reading_num), "")) != ""
                ):

                    # Add 3rd of daily OT w/o Psalms readings

                    previous_book = days_readings[-1][0]
                    current_book = reading[0]
                    # If next reading is in same book, then merge the readings
                    if previous_book == current_book:
                        merged_chapters = f"{days_readings[-1][1]}-{reading[1]}"

                        pattern = r"(\d+)-(\d+)-(\d+)"  # e.g., "1-2-3"
                        match = re.search(pattern, merged_chapters)
                        if match:
                            # Merge chapters like "1-2-3" to chapters like "1-3"
                            merged_chapters = f"{match.group(1)}-{match.group(3)}"

                        days_readings[-1][1] = merged_chapters
                    else:
                        days_readings.append(reading)
                    reading_num += 1

            month_and_day_of_month = f"{date.strftime('%m-%d')}"
            date_and_day = f"{month_and_day_of_month} {day_of_week}"
            ot_wo_psalms[date_and_day] = days_readings

    with open(LIBRARY_DIR / "ot_wo_psalms.json", "w") as json_file:
        json.dump(ot_wo_psalms, json_file, indent=4)

    return ot_wo_psalms


def get_nt_readings(year):

    nt_readings = {}

    with open(LIBRARY_DIR / "nt_chapters.json", "r") as json_file:
        selections = json.load(json_file)

    reading_num = 1

    for days in range(DAYS_IN_YEAR):

        date = THIS_YEAR_START + datetime.timedelta(days=days)
        day_of_week = date.strftime("%a")[:2].replace("Su", "LD")
        if (
            day_of_week not in ("LD", "Sa")
            and (reading := selections.get(str(reading_num), "")) != ""
        ):
            days_readings = [reading]

            reading_num += 1

            month_and_day_of_month = f"{date.strftime('%m-%d')}"
            date_and_day = f"{month_and_day_of_month} {day_of_week}"
            nt_readings[date_and_day] = days_readings

    with open(YEAR_DIR / "nt_readings.json", "w") as json_file:
        json.dump(nt_readings, json_file, indent=4)

    return nt_readings


def get_fpcr_psalm_readings(year):

    fpcr_psalm_readings = {}

    with open(LIBRARY_DIR / "fpcr_psalm_selections.json", "r") as json_file:
        selections = json.load(json_file)

    reading_num = 1

    for days in range(DAYS_IN_YEAR):

        date = THIS_YEAR_START + datetime.timedelta(days=days)
        day_of_week = date.strftime("%a")[:2].replace("Su", "LD")
        if (
            day_of_week != "LD"
            and (reading := selections.get(str(reading_num), "")) != ""
        ):
            days_readings = [reading]

            reading_num += 1

            month_and_day_of_month = f"{date.strftime('%m-%d')}"
            date_and_day = f"{month_and_day_of_month} {day_of_week}"
            fpcr_psalm_readings[date_and_day] = days_readings

    # Since 2022 starts on a Saturday, it has 313 (365 - 52) days
    #   which are not Lord's Days (Sundays).
    # But there are only 312 Psalm selections in the Comprehensive
    #   Psalter.
    # So for Saturday, December 31, 2022, add an extra Psalm selection
    fpcr_psalm_readings["12-31 Sa"] = [["Psalms", "110"]]

    with open(YEAR_DIR / "fpcr_psalm_readings.json", "w") as json_file:
        json.dump(fpcr_psalm_readings, json_file, indent=4)

    return fpcr_psalm_readings


def create_plan_2022():

    bible_book_metadata = get_bible_book_metadata()

    create_library_of_readings(bible_book_metadata)

    ot_wo_psalms = get_ot_wo_psalms(YEAR)

    create_bible_audio_playlist(
        YEAR, bible_book_metadata, ot_wo_psalms, "ot_wo_psalms_playlists"
    )

    create_rtf_and_pdf(
        YEAR,
        ot_wo_psalms,
        "ot_wo_psalms",
        "Reading the Old Testament (except the Psalms)",
    )

    nt_readings = get_nt_readings(YEAR)
    create_bible_audio_playlist(YEAR, bible_book_metadata, nt_readings, "nt_playlists")
    create_rtf_and_pdf(
        YEAR, nt_readings, "nt_readings", "Weekday New Testament Reading"
    )

    fpcr_psalm_readings = get_fpcr_psalm_readings(YEAR)
    create_bible_audio_playlist(
        YEAR, bible_book_metadata, fpcr_psalm_readings, "fpcr_psalm_playlists"
    )
    create_rtf_and_pdf(
        YEAR,
        fpcr_psalm_readings,
        "fpcr_psalm_readings",
        "Reading and Singing Psalm Selections Six Days a Week",
    )

    bible_readings = {}
    add_to_bible_readings(bible_readings, ot_wo_psalms)
    add_to_bible_readings(bible_readings, nt_readings)
    add_to_bible_readings(bible_readings, fpcr_psalm_readings)
    with open(YEAR_DIR / "bible_readings.json", "w") as json_file:
        json.dump(bible_readings, json_file, indent=4)

    create_bible_audio_playlist(
        YEAR, bible_book_metadata, bible_readings, "bible_playlists"
    )

    create_rtf_and_pdf(
        YEAR,
        bible_readings,
        "bible_readings",
        "Daily Bible Reading and Singing",
        abbrev_books=True,
    )


if __name__ == "__main__":
    create_plan_2022()
