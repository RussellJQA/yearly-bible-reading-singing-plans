import datetime
import json
from pathlib import Path

from create_rtf_and_pdf import add_to_bible_readings
from create_rtf_and_pdf import create_rtf_and_pdf
from get_bible_book_metadata import get_bible_book_metadata
from create_library_of_readings import create_library_of_readings
from create_bible_audio_playlist import create_bible_audio_playlist

YEAR = 2021
THIS_YEAR_START = datetime.date(YEAR, 1, 1)
DAYS_IN_YEAR = (datetime.date(YEAR + 1, 1, 1) - THIS_YEAR_START).days
SCRIPT_DIR = Path(__file__).resolve().parent
LIBRARY_DIR = SCRIPT_DIR / "library"
YEAR_DIR = SCRIPT_DIR / str(YEAR)


def get_ot_wo_das_ho_readings(year):

    ot_wo_das_ho_readings = {}

    with open(
            LIBRARY_DIR / "ot_wo_david_and_solomon_hebrew_order_chapters.json",
            "r") as json_file:
        selections = json.load(json_file)

    reading_num = 1

    for days in range(DAYS_IN_YEAR):

        date = THIS_YEAR_START + datetime.timedelta(days=days)
        day_of_week = date.strftime("%a")[:2].replace("Su", "LD")
        days_readings = []

        if (reading := selections.get(str(reading_num), "")) != "":
            days_readings.append(reading)
            reading_num += 1

            if (reading := selections.get(str(reading_num), "")) != "":

                previous_book = days_readings[-1][0]
                current_book = reading[0]

                # If next reading is in same book, then merge the 2 readings
                if previous_book == current_book:
                    days_readings[-1][
                        1] = f"{days_readings[-1][1]}-{reading[1]}"
                else:
                    days_readings.append(reading)

                reading_num += 1

        month_and_day_of_month = f"{date.strftime('%m-%d')}"
        date_and_day = f"{month_and_day_of_month} {day_of_week}"
        ot_wo_das_ho_readings[date_and_day] = days_readings

    # There are only 728 readings in ot_wo_das_ho_readings,
    #   but 2*365=730 are needed for 2021.
    # So for Friday, December 31, 2021, add 2 Psalms which are
    #   quoted or alluded to in Hebrews 1 (the NT reading for the day).
    ot_wo_das_ho_readings["12-31 Fr"] = [["Psalms", "2, 110"]]

    with open(YEAR_DIR / "ot_wo_das_ho_readings.json", "w") as json_file:
        json.dump(ot_wo_das_ho_readings, json_file, indent=4)

    return ot_wo_das_ho_readings


def get_nt_readings(year):

    nt_readings = {}

    with open(LIBRARY_DIR / "nt_chapters.json", "r") as json_file:
        selections = json.load(json_file)

    reading_num = 1

    for days in range(DAYS_IN_YEAR):

        date = THIS_YEAR_START + datetime.timedelta(days=days)
        day_of_week = date.strftime("%a")[:2].replace("Su", "LD")
        days_readings = []

        if day_of_week not in ("LD", "Sa"):  # if Monday to Friday
            if (reading := selections.get(str(reading_num), "")) != "":
                days_readings.append(reading)
                reading_num += 1

        month_and_day_of_month = f"{date.strftime('%m-%d')}"
        date_and_day = f"{month_and_day_of_month} {day_of_week}"
        nt_readings[date_and_day] = days_readings

    # Since 2021 starts on a Friday, it has 261 (52 * 5 + 1) weekdays.
    # But there are only 260 chapters in the New Testament.
    # So for Friday, December 31, 2021, add Hebrews 1.
    nt_readings["12-31 Fr"] = [["Hebrews", "1"]]

    with open(YEAR_DIR / "nt_readings.json", "w") as json_file:
        json.dump(nt_readings, json_file, indent=4)

    return nt_readings


def get_solomon_readings(year):

    solomon_readings = {}

    with open(LIBRARY_DIR / "solomon_chapters.json", "r") as json_file:
        selections = json.load(json_file)

    reading_num = 1

    for days in range(DAYS_IN_YEAR):

        date = THIS_YEAR_START + datetime.timedelta(days=days)
        day_of_week = date.strftime("%a")[:2].replace("Su", "LD")
        days_readings = []

        if day_of_week == "Sa":  # if Saturday
            if (reading := selections.get(str(reading_num), "")) != "":
                days_readings.append(reading)
                reading_num += 1

        month_and_day_of_month = f"{date.strftime('%m-%d')}"
        date_and_day = f"{month_and_day_of_month} {day_of_week}"
        solomon_readings[date_and_day] = days_readings

    # Since 2021 starts on a Friday, it has 52 Saturdays.
    # But there are only 51 chapters in the Writings of Solomon.
    # So for Saturday, December 25, 2021, add Song of Solomon 1.
    solomon_readings["12-25 Sa"] = [["Song of Solomon", "1"]]

    with open(YEAR_DIR / "solomon_readings.json", "w") as json_file:
        json.dump(solomon_readings, json_file, indent=4)

    return solomon_readings


def get_fpcr_psalm_readings(year):

    fpcr_psalm_readings = {}

    with open(LIBRARY_DIR / "fpcr_psalm_selections.json", "r") as json_file:
        selections = json.load(json_file)

    reading_num = 1

    for days in range(DAYS_IN_YEAR):

        date = THIS_YEAR_START + datetime.timedelta(days=days)
        day_of_week = date.strftime("%a")[:2].replace("Su", "LD")
        days_readings = []

        if day_of_week != "LD":  # if not a Lord's Day
            if (reading := selections.get(str(reading_num), "")) != "":
                days_readings.append(reading)
                reading_num += 1

        month_and_day_of_month = f"{date.strftime('%m-%d')}"
        date_and_day = f"{month_and_day_of_month} {day_of_week}"
        fpcr_psalm_readings[date_and_day] = days_readings

    # Since 2021 starts on a Friday, it has 313 (52 * 6 + 1) days
    #   which are not Lord's Days (Sundays).
    # But there are only 312 Psalm selections in the Comprehensive
    #   Psalter.
    # So for Friday, December 31, 2021, add some Psalm selections
    #   quoted or alluded to in Hebrews 1 (the NT reading for the day).
    fpcr_psalm_readings["12-31 Fr"] = [[
        "Psalms", "45:1-7, 102:23-28, 104:1-9"
    ]]

    with open(YEAR_DIR / "fpcr_psalm_readings.json", "w") as json_file:
        json.dump(fpcr_psalm_readings, json_file, indent=4)

    return fpcr_psalm_readings


def create_plan_2021():

    bible_book_metadata = get_bible_book_metadata()

    create_library_of_readings(bible_book_metadata)

    ot_wo_das_ho_readings = get_ot_wo_das_ho_readings(YEAR)
    create_bible_audio_playlist(YEAR_DIR, bible_book_metadata,
                                ot_wo_das_ho_readings,
                                "ot_wo_das_ho_playlists")
    create_rtf_and_pdf(
        YEAR, ot_wo_das_ho_readings, "ot_wo_das_ho_readings",
        "Reading the Old Testament (without the Writings of David and "
        "Solomon), in Hebrew OT order")

    nt_readings = get_nt_readings(YEAR)
    create_bible_audio_playlist(YEAR_DIR, bible_book_metadata, nt_readings,
                                "nt_playlists")
    create_rtf_and_pdf(YEAR, nt_readings, "nt_readings",
                       "Weekday New Testament Reading")

    solomon_readings = get_solomon_readings(YEAR)
    create_bible_audio_playlist(YEAR_DIR, bible_book_metadata,
                                solomon_readings, "solomon_playlists")
    create_rtf_and_pdf(YEAR, solomon_readings, "solomon_readings",
                       "Reading the Writings of Solomon on Saturdays")

    fpcr_psalm_readings = get_fpcr_psalm_readings(YEAR)
    create_bible_audio_playlist(YEAR_DIR, bible_book_metadata,
                                fpcr_psalm_readings, "fpcr_psalm_playlists")
    create_rtf_and_pdf(YEAR, fpcr_psalm_readings, "fpcr_psalm_readings",
                       "Reading and Singing Psalm Selections Six Days a Week")

    bible_readings = {}
    add_to_bible_readings(bible_readings, ot_wo_das_ho_readings)
    add_to_bible_readings(bible_readings, nt_readings)
    add_to_bible_readings(bible_readings, solomon_readings)
    add_to_bible_readings(bible_readings, fpcr_psalm_readings)
    with open(YEAR_DIR / "bible_readings.json", "w") as json_file:
        json.dump(bible_readings, json_file, indent=4)
    create_bible_audio_playlist(YEAR_DIR, bible_book_metadata, bible_readings,
                                "bible_playlists")
    create_rtf_and_pdf(YEAR,
                       bible_readings,
                       "bible_readings",
                       "Daily Bible Reading and Singing",
                       abbrev_books=True)


if __name__ == "__main__":
    create_plan_2021()
