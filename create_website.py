import os
from pathlib import Path
import string

import markdown2

SCRIPT_DIR = Path(__file__).resolve().parent
GITHUB_PAGES_DIR = SCRIPT_DIR / "github_pages"

with open("template.html", "r", encoding="utf-8") as read_file:
    TEMPLATE_STRING = read_file.read()


def markdown_to_html(md_basename, html_basename, title):

    with open(SCRIPT_DIR / f"{md_basename}.md", "r") as read_file:
        html_source = read_file.read()
    html_source = html_source.replace(".md", ".html")
    html_source = html_source.replace(
        "(2021/",
        "(https://github.com/RussellJQA/yearly-bible-reading-singing-plans/blob/main/2021/"
    )
    main_html = markdown2.markdown(html_source)

    html_template = string.Template(TEMPLATE_STRING)
    with open(GITHUB_PAGES_DIR / f"{html_basename}.html",
              "w",
              encoding="utf-8",
              newline="") as write_file:
        output = html_template.substitute(title=title, main_html=main_html)
        write_file.write(output)


def create_website(year):
    os.makedirs(GITHUB_PAGES_DIR, exist_ok=True)
    markdown_to_html("README", "index", "Yearly Bible Reading/Singing Plans")
    markdown_to_html("meter", "meter", "Meter")
    markdown_to_html("psalms_of_david_in_metre", "psalms_of_david_in_metre",
                     "The Psalms of David in Metre")


if __name__ == "__main__":
    create_website("2021")
