"""
Adjusts hyperlinks and text across all readme files so that they "agree" with each other.

Rather than updating files individually, this script is updated and re-run per update, which then modifies all readmes.

Author: Daniel "Speyedr" Summer
"""

from re import compile, search
from os import scandir, getcwd, chdir  # scandir for getting language codes, getcwd and chdir for working directory fix

UTILITY_FOLDER = "\\" + "util"
working_dir = getcwd()

# directory hotfix: allows running script from inside util folder
if working_dir.endswith(UTILITY_FOLDER):
    chdir(working_dir[:-len(UTILITY_FOLDER)])   # Go up one folder (by trimming the utility folder from absolute path)


class Author:
    """Simple record-keeping class"""

    def __init__(self, alias, promotional_link, language_translated):
        self.alias = alias
        self.url = promotional_link
        self.language = language_translated

    def __str__(self):
        return self.get_markdown_embed()

    def get_markdown_embed(self):
        return "[" + self.alias + "](" + self.url + ") (" + self.language + ")"


TRANSLATION_FOLDER = "translations"

# Promotional URLs are currently just GitHub links but can be changed to any other link on request.
TRANSLATION_CREDITS = [
                        Author("coeurGG", "https://github.com/coeurGG", "French"),
                        Author("Foxie117", "https://github.com/Foxie1171", "Russian"),
                        Author("TKMachine", "https://github.com/TKMachine", "Romanian"),
                        Author("Kyeki", "https://github.com/Kyekii", "Spanish"),
                        Author("jorgex", "https://github.com/jorgex94", "Spanish"),
                        Author("Rav1sh", "https://github.com/Rav1sh", "Dutch")
                      ]

# Key is ISO 639-1 language code (which is also the name of the folder), value is name of the language.
# Is there even a need to do this? Can't we just get an ISO 639-1 library / lookup table from somewhere?
# TODO: Search directories to figure out the ISO codes for current languages
LANGUAGES = {
                "EN": "English",
                "ES": "Spanish",
                "FR": "French",
                "RU": "Russian",
                "RO": "Romanian",
                #"NL": "Dutch"
}

LANGUAGE_FOLDERS = [file.path for file in scandir(TRANSLATION_FOLDER) if file.is_dir()]
print(LANGUAGE_FOLDERS)

LANGUAGE_CODES = [directory[len(TRANSLATION_FOLDER)+1:] for directory in LANGUAGE_FOLDERS]  # get the language codes

# TRANSLATIONS.items() returns array of tuples where [0] is key (ISO 639-1 code) and [1] is value (name of language).
# sorted() sorts an array of items based on a key, which in this case is a function which simply returns [1], the value.
# i.e. TRANSLATIONS is now a sorted array of tuples, in ascending alphabetical order on the name of the language.
LANGUAGES = [(key, value) for (key, value) in sorted(LANGUAGES.items(), key=lambda x: x[1])]

LANGUAGES_HEADER_LINE = 2    # 3rd line in the file is where the Language header goes.

# Matches all characters part of the credits section.
# Find the coeurGG line, keep going until we see the next header in the README file.
FIND_CREDITS_SECTION = compile(r"[-*] \[coeurGG](?:.|\r|\n)*(?=##)")


def generate_credits_list(list_of_authors=None):
    if list_of_authors is None:
        list_of_authors = TRANSLATION_CREDITS

    ret = ""
    for author in list_of_authors:
        ret += author.get_markdown_embed() + "\n"

    return ret + "\n"


def generate_url_to_file(linked_readme_language, this_readme_language="EN"):
    if linked_readme_language == this_readme_language: return "README.md"   # We're already at this file

    return ("translations/" if this_readme_language == "EN" else "../") + \
           ("../" if linked_readme_language == "EN" else linked_readme_language + "/") + \
            "README.md"


def generate_readme_header_links(this_readme_language="EN", header_separator=" | "):
    ret = []
    for (iso_code, name) in LANGUAGES:
        if iso_code == this_readme_language:
            ret.append(name)
        else:
            ret.append("["+name+"]("+generate_url_to_file(iso_code, this_readme_language)+")")  # Save name, add link

    return header_separator.join(ret)


if __name__ == "__main__":
    # Relative links are in the context of the base directory, which is where the English README file is.
    files = [(generate_url_to_file(iso_code, "EN"), iso_code, name) for (iso_code, name) in LANGUAGES]
    # Read file, overwrite 3rd line (should maybe do a regex instead to find the target line?)
    for (file, iso_code, name) in files:
        print(file)
        #handle = open("../translations/ES/README.md")
        handle = open(file, "r", encoding="utf-8")            # read as bytes to prevent python from decoding "invalid bytes"
        content = handle.read()              # read all of it
        handle.close()
        lines = content.splitlines(False)    # split by lines
        #print(lines)
        lines[LANGUAGES_HEADER_LINE] = generate_readme_header_links(iso_code)   # generate header and replace
        print(lines[LANGUAGES_HEADER_LINE])  # test print
        content = '\n'.join(lines)           # rejoin lines for next scan as it goes across several lines
        (credits_start, credits_end) = search(FIND_CREDITS_SECTION, content).span()  # find the credits section
        content = content[:credits_start] + generate_credits_list() + content[credits_end:]  # replace with new credits
        #print(content)                       # another test print