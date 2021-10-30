import datetime
from pathlib import Path
import re
from zipfile import ZipFile

# For each day of the plan, create .m3u playlists to play the
# corresponding .mp3 files from OT and NT CDs of KJV Bible audio from
# Talking Bibles International (https://www.talkingbibles.org/)
#
"""
The Old Testament
KJV
MP3-CD
Genesis - Job
0096003-OT-79
Copyright Public Domain
King James Version
CD #1 and #2
Talking Bibles International
Escondido, CA 92033
"""
#
"""
The New Testament...
...
0096-03-NT-70
Public Domain
...
"""


def get_bible_chapter_mp3_path(ot_or_nt, book_num_and_name, chapter):
    if book_num_and_name == "22_song-of-solomon":
        book_num_and_name = "22_songofsolomon"
    folder = Path(ot_or_nt) / book_num_and_name
    in_ot = ot_or_nt == "ot"
    # Don't include chapter numbers for books with only 1 chapter
    if book_num_and_name in (
        "31_obadiah",
        "18_philemon",
        "24_2-john",
        "25_3-john",
        "26_jude",
    ):
        fn = f"{book_num_and_name}.mp3"
    else:
        # Zero-pad chapter numbers
        chapter = f"{int(chapter):03}" if in_ot else f"{int(chapter):02}"
        fn = f"{book_num_and_name}_{chapter}.mp3"
    return folder / fn


# NOTE: Commented with "# # " below, because when I used a triple-quoted
# string, flake8 complained with 19 "invalid escape sequence" messages.
# # For more info, see: https://en.wikipedia.org/wiki/M3U#Extended_M3U
# # # Example MP3 playlist (03-02-Tu.m3u):
# # #EXTM3U
# # #PLAYLIST:Tuesday, 02 March 2021
# # #EXTALB: KJV Bible
# # #EXTART: Talking Bibles International
# # #EXTGENRE:Speech
# # #EXTINF:0,Numbers 4
# # \storage\emulated\0\Music\TBAudio\ot\04_numbers\04_numbers_004.mp3
# # #EXTINF:0,Numbers 5
# # \storage\emulated\0\Music\TBAudio\ot\04_numbers\04_numbers_005.mp3
# # #EXTINF:0,Mark 15
# # \storage\emulated\0\Music\TBAudio\nt\02_mark\02_mark_15.mp3
# # #EXTINF:0,Psalm 30
# # \storage\emulated\0\Music\TBAudio\ot\19_psalms\19_psalms_030.mp3


def create_bible_audio_playlist(year, bible_book_metadata, readings, readings_fn):

    SCRIPT_DIR = Path(__file__).resolve().parent
    YEAR_DIR = SCRIPT_DIR / str(year)

    with ZipFile(YEAR_DIR / f"{readings_fn}.zip", "w") as playlists_file:

        M3U_DIR = YEAR_DIR / readings_fn
        M3U_DIR.mkdir(exist_ok=True)

        for date, days_readings in readings.items():

            long_date = datetime.date(
                int(year), int(date[0:2]), int(date[3:5])
            ).strftime("%A, %d %B %Y")

            m3u_fn = M3U_DIR / f"{date.replace(' ', '-')}.m3u"
            with open(m3u_fn, "w") as m3u_file:
                m3u_file.write("#EXTM3U\n")
                m3u_file.write(f"#PLAYLIST:{long_date}\n")
                m3u_file.write("#EXTALB: KJV Bible\n")
                m3u_file.write("#EXTART: Talking Bibles International\n")
                m3u_file.write("#EXTGENRE:Speech\n")

                for reading in days_readings:
                    book = reading[0]
                    book_num = bible_book_metadata[book]["book_num"]
                    if int(book_num) < 40:
                        ot_or_nt = "ot"
                    else:
                        ot_or_nt = "nt"
                        book_num = f"{(int(book_num) - 39):02}"
                    book_num_and_name = book_num + f"_{book.lower().replace(' ', '-')}"
                    chapters_and_verses = list(str(reading[1]).split(", "))
                    # Use a regex to remove verse references
                    #   30:1-7a -> 30
                    #   30:7b-12 -> 30
                    #   139:11-16a -> 139
                    #   139:16b-24 -> 139
                    # "[ab]?"" means 0 or 1 "a" or "b"
                    pattern = r"(.*)(:\d{1,3}[ab]?-\d{1,3}[ab]?)"
                    for chapter_and_verse in chapters_and_verses:
                        match = re.search(pattern, chapter_and_verse)
                        chapter = match.group(1) if match else chapter_and_verse

                        match = re.search(r"(\d{1,3})-(\d{1,3})", chapter)
                        if match:
                            chapter1 = f"{match.group(1)}"
                            path = get_bible_chapter_mp3_path(
                                ot_or_nt, book_num_and_name, chapter1
                            )
                            m3u_file.write(f"#EXTINF:0,{book} {chapter1}\n")
                            m3u_file.write(f"{path}\n")
                            chapter2 = f"{match.group(2)}"
                            path = get_bible_chapter_mp3_path(
                                ot_or_nt, book_num_and_name, chapter2
                            )
                            m3u_file.write(f"#EXTINF:0,{book} {chapter2}\n")
                        else:
                            path = get_bible_chapter_mp3_path(
                                ot_or_nt, book_num_and_name, chapter
                            )
                            m3u_file.write(f"#EXTINF:0,{book} {chapter}\n")
                        m3u_file.write(f"{path}\n")

            m3u_basename_with_ext = f"{m3u_fn.stem}.m3u"
            playlists_file.write(m3u_fn, arcname=m3u_basename_with_ext)
