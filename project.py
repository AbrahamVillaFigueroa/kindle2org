import sys
import re
from datetime import datetime

def main():
    if len(sys.argv) < 3:
        sys.exit("Not enough arguments")
    if len(sys.argv) > 3:
        sys.exit("Too many arguments")
    if not sys.argv[1].endswith(".txt"):
        sys.exit("Select an existing 'My Clippings.txt' file as input")
    if not sys.argv[2].endswith(".org"):
        sys.exit("Select an Org File as output")

    with open(f"{sys.argv[1]}") as kindle_clippings, open(f"{sys.argv[2]}", "w") as org_file:
        lines = kindle_clippings.readlines()
        list_of_entries = split_entries(lines)
        titles_with_note_location = get_titles_with_notes(list_of_entries)

        list_highlights = []
        list_highlights_for_notes = []
        for entry in list_of_entries:
            if get_type(entry[2]) == "Highlight" and entry_belongs_to_note(entry, titles_with_note_location) == None:
                dict_entry = make_dict_highlight_entry(entry)
                list_highlights.append(dict_entry)
            elif get_type(entry[2]) == "Highlight" and entry_belongs_to_note(entry, titles_with_note_location) == True:
                dict_entry_for_note = make_dict_highlight_entry(entry)
                list_highlights_for_notes.append(dict_entry_for_note)
            else:
                pass

        list_notes = []
        for entry in list_of_entries:
            if get_type(entry[2]) == "Note":
                dict_entry = [
                    f"* {get_title(entry[1])} | {get_author(entry[1])}",
                    f"*** {entry[4]}"
                    f"#+begin_quote{get_quote(entry, list_highlights_for_notes)}#+end_quote\n",
                ]
                list_notes.append(dict_entry)
            else:
                pass

        list_bookmarks = []
        for entry in list_of_entries:
            if get_type(entry[2]) == "Bookmark":
                dict_entry = [
                    f"* {get_title(entry[1])} | {get_author(entry[1])}",
                    f"- Location {get_location(entry[2])}, page {get_page(entry[2])}, made on {get_date(entry[2])}\n"
                ]
                list_bookmarks.append(dict_entry)
            else:
                pass

        dict_highlights_per_title = make_master_dic(list_highlights)
        dict_notes_per_title = make_master_dic(list_notes)
        dict_bookmarks_per_title = make_master_dic(list_bookmarks)

        all_title_authors_list = []
        for entry in list_of_entries:
            title_plus_author = f"* {get_title(entry[1])} | {get_author(entry[1])}"
            if title_plus_author not in all_title_authors_list:
                all_title_authors_list.append(title_plus_author)

        master_dictionary = {}
        for title in all_title_authors_list:
            master_dictionary[title]= {
                "notes":[],
                "highlights":[],
                "bookmarks":[],
            }

        for title in master_dictionary.keys():
            if title in dict_notes_per_title.keys():
                master_dictionary[title]["notes"].extend(dict_notes_per_title[title])

        for title in master_dictionary.keys():
            if title in dict_highlights_per_title.keys():
                  master_dictionary[title]["highlights"].extend(dict_highlights_per_title[title])

        for title in master_dictionary.keys():
            if title in dict_bookmarks_per_title.keys():
                  master_dictionary[title]["bookmarks"].extend(dict_bookmarks_per_title[title])

        org_file.write(f"#+title: My Kindle Clippings"
                       f"\n#+startup: overview"
                       f"\n#+date_of_import: {datetime.today().strftime('%Y-%m-%d')}\n \n")


        for title in all_title_authors_list:
            org_file.write(f"{title}\n")
            if title in dict_notes_per_title.keys():
                org_file.write(f"** Notes\n")
                for i in master_dictionary[title]['notes']:
                    org_file.write(f"{i}")
            if title in dict_highlights_per_title.keys():
                org_file.write(f"** Highlights\n")
                for j in master_dictionary[title]['highlights']:
                    org_file.write(f"{j}")
            if title in dict_bookmarks_per_title.keys():
                org_file.write(f"** Bookmarks\n")
                for k in master_dictionary[title]['bookmarks']:
                    org_file.write(f"{k}")

def make_master_dic(entries_list):
    dictionary = {}
    for i in range(len(entries_list)):
        if entries_list[i][0] in dictionary:
            dictionary[entries_list[i][0]].append(entries_list[i][1])
        else:
            dictionary[entries_list[i][0]]= []
            dictionary[entries_list[i][0]].append(entries_list[i][1])
    return dictionary

def get_quote(entry, list_highlights_for_notes):
    location_note = get_location(entry[2])
    title_note = f"* {get_title(entry[1])} | {get_author(entry[1])}"
    for highlight in list_highlights_for_notes:
        if highlight[0] == title_note:
            if location_note == get_location_of_highlight(highlight[1]):
                return extract_quote(highlight[1])

def extract_quote(text):
    match_type = re.search(r".*#\+begin_quote(.*)#\+end_quote", text, re.DOTALL)
    return match_type.group(1)

def get_location_of_highlight(text):
    match_location = re.search(r".*Location [0-9]*-(.*),", text, re.DOTALL)
    return match_location.group(1)

def make_dict_highlight_entry(entry):
    return [f"* {get_title(entry[1])} | {get_author(entry[1])}",
            f"*** Made on {get_date(entry[2])}\n"
            f"#+begin_quote\n{entry[4]}—Location {get_location(entry[2])}, page {get_page(entry[2])}\n#+end_quote\n"]

def entry_belongs_to_note(entry, titles_with_note_location):
    location = get_location(entry[2])
    start_quote, end_quote = get_location(entry[2]).split("-")
    title = get_title(entry[1])
    for i in titles_with_note_location:
       if i[0] == title:
           if i[1] == end_quote:
               return True

def split_entries(lines):
    list_of_entries = []
    separator = "==========\n"
    start = 0
    counter = 1
    for index, entry in enumerate(lines):
        if entry == separator:
            list_of_entries.append(lines[start:index])
            start = index + 1
    for i in list_of_entries:
        i.insert(0, counter)
        counter += 1
    return list_of_entries

def get_titles_with_notes(list_of_entries):
    notes_title = []
    loc_of_note = []
    for entry in list_of_entries:
        if get_type(entry[2]) == "Note":
            notes_title.append(get_title(entry[1]))
            loc_of_note.append(get_location(entry[2]))
    titles_with_note_location = []
    for i in range(len(notes_title)):
        list = [notes_title[i], loc_of_note[i]]
        titles_with_note_location.append(list)
    return titles_with_note_location

def get_title(text):
    match_title = re.search(r"(^.*) \(.*", text)
    return match_title.group(1)

def get_author(text):
    match_author = re.search(r"^.*\((.*)\)$", text)
    return match_author.group(1)

def get_type(text):
    match_type = re.search(r"^- Your (.*?) on.*$", text)
    return match_type.group(1)

def get_date(text):
    match_date = re.search(r"Added on (.*)$", text)
    return match_date.group(1)

def get_location(text):
    match_location = re.search(r"Location ([0-9]*(?:-[0-9]*)?) ", text)
    return match_location.group(1)

def get_page(text):
    match_page = re.search(r"on page ([0-9]*)", text)
    if match_page:
        return match_page.group(1)
    else:
        return "-"

if __name__ == "__main__":
    main()
