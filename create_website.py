import os
from pathlib import Path
import string

import markdown2

SCRIPT_DIR = Path(__file__).resolve().parent
GITHUB_PAGES_DIR = SCRIPT_DIR / "github_pages"

with open("template.html", "r", encoding="utf-8") as read_file:
    TEMPLATE_STRING = read_file.read()


def markdown_to_html(md_basename, html_basename, title, description):

    with open(SCRIPT_DIR / f"{md_basename}.md", "r") as read_file:
        html_source = read_file.read()
    html_source = html_source.replace(".md", ".html")
    html_source = html_source.replace(
        "(2021/", "(https://github.com/RussellJQA/"
        "yearly-bible-reading-singing-plans/blob/main/2021/")
    main_html = markdown2.markdown(html_source)

    # HTML link to "<h2>2021...</h2>"" anchor on the same HTML page
    main_html = main_html.replace(
        "<a href=\"##-2021-bible-reading-and-singing-plan\">",
        "<a href=\"#2021-bible-reading-and-singing-plan\">")
    # Linked-to "<h2>2021...</h2>"" anchor
    main_html = main_html.replace(
        "<h2>2021", "<h2 id='2021-bible-reading-and-singing-plan'>2021")

    html_template = string.Template(TEMPLATE_STRING)
    with open(GITHUB_PAGES_DIR / f"{html_basename}.html",
              "w",
              encoding="utf-8",
              newline="") as write_file:
        output = html_template.substitute(title=title,
                                          description=description,
                                          main_html=main_html)
        write_file.write(output)


def create_website(year):
    os.makedirs(GITHUB_PAGES_DIR, exist_ok=True)
    markdown_to_html(
        "README", "index", "Yearly Bible Reading/Singing Plans",
        "Yearly Bible Reading/Singing Plans. Starting with 2020, "
        "has downloadable PDF plan(s) for reading thru the Bible,"
        " and singing thru the Psalms, in 1 year.")
    markdown_to_html(
        "meter", "meter", "Meter",
        "Info about meter -- patterns of syllables used in English "
        "poetry and song. Metrical Psalms are often written in Common "
        "Meter, Short Meter, or Long Meter.")
    markdown_to_html(
        "psalms_of_david_in_metre", "psalms_of_david_in_metre",
        "The Psalms of David in Metre",
        "Info about printed and online editions -- and mobile apps -- "
        "of 'The Psalms of David in Metre', a.k.a 'The 1650 Scottish "
        "Psalter' and 'Scottish Psalmody'.")


if __name__ == "__main__":
    create_website("2021")
