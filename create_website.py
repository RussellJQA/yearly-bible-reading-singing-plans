import os
from pathlib import Path
import shutil
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
    main_html = markdown2.markdown(html_source)

    html_template = string.Template(TEMPLATE_STRING)
    with open(GITHUB_PAGES_DIR / f"{html_basename}.html",
              "w",
              encoding="utf-8",
              newline="") as write_file:
        output = html_template.substitute(title=title, main_html=main_html)
        write_file.write(output)


def create_website(year):
    gh_year_dir = GITHUB_PAGES_DIR / year
    os.makedirs(gh_year_dir, exist_ok=True)
    year_dir = SCRIPT_DIR / year
    pdf_files = year_dir.glob("*.pdf")
    for pdf_file in pdf_files:
        shutil.copy(pdf_file, gh_year_dir)

    markdown_to_html("README", "index", "Yearly Bible Reading/Singing Plans")
    markdown_to_html("meter", "meter", "Meter")
    markdown_to_html("psalms_of_david_in_metre", "psalms_of_david_in_metre",
                     "The Psalms of David in Metre")


if __name__ == "__main__":
    create_website("2021")
