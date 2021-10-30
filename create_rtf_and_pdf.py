from dataclasses import dataclass
import datetime
import os
from pathlib import Path
import string
import subprocess

from get_bible_book_metadata import get_bible_book_metadata

SCRIPT_DIR = Path(__file__).resolve().parent


def create_rtf_and_pdf(
    year, daily_readings, output_basename, title, abbrev_books=False
):
    """Create RTF and PDF files containing the specified readings"""

    @dataclass  # See https://realpython.com/python-data-classes/
    class Month:
        heading: str  # Month/Year, like January 2021, February 2021, etc.
        readings: str

    year_dir = SCRIPT_DIR / str(year)

    month_data = [
        Month(
            heading=f"{datetime.date(year, int(month), 1).strftime('%B')} {year}",
            readings="",
        )
        for month in range(1, 13)  # readings initially blank
    ]

    bible_book_abbrevs = {
        book_name: data["logos_most_common_abbrev"]
        for book_name, data in get_bible_book_metadata().items()
    }

    previous_month = None
    for date, daily_reading in daily_readings.items():
        if (month := int(date[:2])) != previous_month:
            previous_month = month
        reading = r"{\b " + date[3:] + ": }"
        passages = []
        for passage in daily_reading:
            book_name = passage[0]
            book = bible_book_abbrevs[book_name] if abbrev_books else book_name
            if book == "Psalms":
                book = "Psalm"  # References to the Psalms should use "Psalm"
            chapter_and_verse = passage[1]
            passages.append(f"{book} {chapter_and_verse}")
        reading += ", ".join(passages)
        line_or_no_line = "\\line " if month_data[month - 1].readings else ""
        month_data[month - 1].readings += f"{line_or_no_line}\\ql {reading}"

    with open(year_dir / "bible_plan_template.rtf", "r", encoding="utf-8") as read_file:
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
    libreoffice_path = (
        Path(os.environ.get("ProgramW6432")) / "LibreOffice" / "program" / "soffice.exe"
    )
    # If LibreOffice is installed in the default Windows location ...
    if libreoffice_path.exists():
        subprocess.run(
            [
                str(libreoffice_path),
                "--headless",
                "--convert-to",
                "pdf",
                daily_readings_rtf_fn,
            ],
            cwd=str(year_dir),
        )
    else:
        print(
            "\nSince LibreOffice is not installed in the expected location",
            f"({libreoffice_path})",
            "you'll need to use another means to convert",
            f"{daily_readings_rtf_fn} to a .pdf file.",
        )


def add_to_bible_readings(daily_readings, readings):
    """Add the specified group of readings (NT, Psalms, etc.)
    to the year's collected daily_readings"""
    for date, reading in readings.items():
        if len(reading):
            if date in daily_readings:
                daily_readings[date].append(reading[0])
            else:
                daily_readings[date] = reading
        elif date not in daily_readings:
            daily_readings[date] = []
