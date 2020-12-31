from dataclasses import dataclass
import datetime
import os
from pathlib import Path
import string
import subprocess

from get_bible_book_metadata import get_bible_book_metadata
from create_library_of_readings import create_library_of_readings
from get_daily_readings_2021 import (get_bible_readings,
                                     get_ot_wo_das_ho_readings,
                                     get_nt_readings, get_solomon_readings,
                                     get_fpcr_psalm_readings)

bible_book_metadata = get_bible_book_metadata()
bible_book_abbrevs = {}
for book_name, data in bible_book_metadata.items():
    bible_book_abbrevs[book_name] = data["logos_most_common_abbrev"]
create_library_of_readings(bible_book_metadata)


@dataclass  # See https://realpython.com/python-data-classes/
class Month:
    heading: str  # Month/Year, like January 2021, February 2021, etc.
    readings: str


def create_rtf_and_pdf(year, daily_readings, output_basename, title):

    month_data = [
        Month(heading=
              f"{datetime.date(year, int(month), 1).strftime('%B')} {year}",
              readings="")
        for month in range(1, 13)  # readings initially blank
    ]

    previous_month = None
    for date, daily_reading in daily_readings.items():
        if (month := int(date[:2])) != previous_month:
            previous_month = month
        reading = r"{\b " + date[3:] + ": }"
        passages = []
        for passage in daily_reading:
            book_name = passage[0]
            book_abbrev = bible_book_abbrevs[book_name]
            chapter_and_verse = passage[1]
            passages.append(f"{book_abbrev} {chapter_and_verse}")
        reading += ", ".join(passages)
        line_or_no_line = "\\line " if month_data[month - 1].readings else ""
        month_data[month - 1].readings += f"{line_or_no_line}\\ql {reading}"

    script_dir = Path(__file__).resolve().parent
    year_dir = script_dir / str(year)

    with open(year_dir / "bible_plan_template.rtf", "r",
              encoding="utf-8") as read_file:
        template_string = read_file.read()
    rtf_template = string.Template(template_string)

    daily_readings_rtf_fn = f"{output_basename}.rtf"
    kwargs = {"title": title}
    for i in range(12):
        kwargs[f"heading{i}"] = month_data[i].heading
        kwargs[f"readings{i}"] = month_data[i].readings
    with open(year_dir / daily_readings_rtf_fn, "w") as rtf_file:
        # Unpack from kwargs dictionary:
        #   kwargs["title"] = title
        #   kwargs["heading0"] = month[0].heading
        #   kwargs["readings0"] = month[0].readings
        #   ...
        # into keyword arguments of substitute():
        #   title = title
        #   heading0 = month_data[0].heading,
        #   readings0 = month_data[0].readings,
        #   ...
        # See
        #  stackabuse.com/formatting-strings-with-the-python-template-class/
        output = rtf_template.substitute(**kwargs)
        rtf_file.write(output)

    # Programmatically convert .rtf to .pdf using LibreOffice. See:
    #   stackoverflow.com/questions/29637626/converting-rtf-to-pdf-using-python
    #     and https://docs.python.org/3/library/subprocess.html
    libreoffice_path = Path(os.environ.get(
        "ProgramW6432")) / "LibreOffice" / "program" / "soffice.exe"
    # If LibreOffice is installed in the default Windows location ...
    if libreoffice_path.exists():
        subprocess.run([
            str(libreoffice_path), "--headless", "--convert-to", "pdf",
            daily_readings_rtf_fn
        ],
                       cwd=str(year_dir))


YEAR = 2021

ot_wo_das_ho_readings = get_ot_wo_das_ho_readings(YEAR)
create_rtf_and_pdf(
    YEAR, ot_wo_das_ho_readings,
    "ot_wo_david_and_solomon_hebrew_order_ho_readings",
    "Reading the Old Testament (without the Writings of David and Solomon), "
    "in Hebrew OT order")

nt_readings = get_nt_readings(YEAR)
create_rtf_and_pdf(YEAR, nt_readings, "nt_readings",
                   "Weekday New Testament Reading")

solomon_readings = get_solomon_readings(YEAR)
create_rtf_and_pdf(YEAR, solomon_readings, "solomon_readings",
                   "Reading the Writings of Solomon on Saturdays")

fpcr_psalm_readings = get_fpcr_psalm_readings(YEAR)
create_rtf_and_pdf(YEAR, fpcr_psalm_readings, "fpcr_psalm_readings",
                   "Reading and Singing Psalm Selections Six Days a Week")

bible_readings = get_bible_readings()
create_rtf_and_pdf(YEAR, bible_readings, "bible_readings",
                   "Daily Bible Reading and Singing")
