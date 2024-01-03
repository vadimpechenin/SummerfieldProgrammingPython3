import os
import pickle
import shelve
import sys
import datetime
import xml.etree.ElementTree
import xml.parsers.expat
import xml.sax.saxutils
import json

from common_utils import Util_adaptive, Console_adaptive

DISPLAY_LIMIT = 20
def main():
    functions = dict(a=add_dvd, e=edit_dvd, l=list_dvds,
                     r=remove_dvd, i=import_, x=export, q=quit)

    filename = os.path.join(os.path.dirname(__file__), "dvds_adaptive.dbm")
    try:
        db = shelve.open(filename, protocol=pickle.HIGHEST_PROTOCOL)
        action = ""
        while True:
            print("\nDVDs ({0})".format(os.path.basename(filename)))
            if action != "l" and 1 <= len(db) < DISPLAY_LIMIT:
                list_dvds(db)
            else:
                print("{0} dvd{1}".format(len(db), Util_adaptive.s(len(db))))
            print()
            menu = ("(A)dd  (E)dit  (L)ist  (R)emove  (I)mport  "
                    "e(X)port  (Q)uit"
                    if len(db) else "(A)dd  (I)mport  (Q)uit")
            valid = frozenset("aelrixq" if len(db) else "aiq")
            action = Console_adaptive.get_menu_choice(menu, valid,
                                             "l" if len(db) else "a", True)
            functions[action](db)
    finally:
        if db is not None:
            db.close()

def list_dvds(db):
    start = ""
    if len(db) > DISPLAY_LIMIT:
        start = Console_adaptive.get_string("List those starting with "
                                   "[Enter=all]", "start")
    print()
    for title in sorted(db, key=str.lower):
        if not start or title.lower().startswith(start.lower()):
            director, year, duration = db[title]
            print("{title} ({year}) {duration} minute{0}, by "
                  "{director}".format(Util_adaptive.s(duration), **locals()))

def add_dvd(db):
    title = Console_adaptive.get_string("Title", "title")
    if not title:
        return
    director = Console_adaptive.get_string("Director", "director")
    if not director:
        return
    year = Console_adaptive.get_integer("Year", "year", minimum=1896,
                               maximum=datetime.date.today().year)
    duration = Console_adaptive.get_integer("Duration (minutes)", "minutes",
                                   minimum=0, maximum=60 * 48)
    db[title] = (director, year, duration)
    db.sync()

def edit_dvd(db):
    old_title = find_dvd(db, "edit")
    if old_title is None:
        return
    title = Console_adaptive.get_string("Title", "title", old_title)
    if not title:
        return
    director, year, duration = db[old_title]
    director = Console_adaptive.get_string("Director", "director", director)
    if not director:
        return
    year = Console_adaptive.get_integer("Year", "year", year, 1896,
                               datetime.date.today().year)
    duration = Console_adaptive.get_integer("Duration (minutes)", "minutes",
                                   duration, minimum=0, maximum=60 * 48)
    db[title] = (director, year, duration)
    if title != old_title:
        del db[old_title]
    db.sync()

def remove_dvd(db):
    title = find_dvd(db, "remove")
    if title is None:
        return
    ans = Console_adaptive.get_bool("Remove {0}?".format(title), "no")
    if ans:
        del db[title]
        db.sync()

def import_(db):
    filename = Console_adaptive.get_string("Import from", "filename")
    if not filename:
        return
    try:
        with open(filename) as json_file:
            data = json.load(json_file)
    except (EnvironmentError) as err:
        print("ERROR:", err)
        return
    db.clear()
    for title in data:
        try:
            year = int(data.get(title).get("year"))
            duration = int(data.get(title).get("duration"))
            director = data.get(title).get("director")
            db[title] = (director, year, duration)
        except ValueError as err:
            print("ERROR:", err)
            return
    print("Imported {0} dvd{1}".format(len(db), Util_adaptive.s(len(db))))
    db.sync()

def export(db):
    filename = os.path.join(os.path.dirname(__file__), "dvds_adaptive.json")
    try:
        with open(filename, "w", encoding="utf8") as outfile:
            dict={}
            for title in sorted(db, key=str.lower):
                director, year, duration = db[title]
                dict[title] = {'director': director, 'year': year,
                               'duration': duration}
            json_string = json.dumps(dict)
            print(json_string)
            outfile.write(json_string)
            print("exported {0} dvd{1} to {2}".format(
                len(db), Util_adaptive.s(len(db)), filename))
            return True
    except:
        return False

def quit(db):
    print("Saved {0} dvd{1}".format(len(db), Util_adaptive.s(len(db))))
    db.close()
    sys.exit()

def find_dvd(db, message):
    message = "(Start of) title to " + message
    while True:
        matches = []
        start = Console_adaptive.get_string(message, "title")
        if not start:
            return None
        for title in db:
            if title.lower().startswith(start.lower()):
                matches.append(title)
        if len(matches) == 0:
            print("There are no dvds starting with", start)
            continue
        elif len(matches) == 1:
            return matches[0]
        elif len(matches) > DISPLAY_LIMIT:
            print("Too many dvds start with {0}; try entering "
                  "more of the title".format(start))
            continue
        else:
            matches = sorted(matches, key=str.lower)
            for i, match in enumerate(matches):
                print("{0}: {1}".format(i + 1, match))
            which = Console_adaptive.get_integer("Number (or 0 to cancel)",
                                        "number", minimum=1, maximum=len(matches))
            return matches[which - 1] if which != 0 else None

main()