"""
Adjusts hyperlinks and text across all readme files so that they "agree" with each other.

Rather than updating files individually, this script is updated and re-run per update, which then modifies all readmes.

IMPORTANT: Run this script from the base directory, NOT the util directory. e.g. `python util/sync_readme.py`

Author: Daniel "Speyedr" Summer
"""

from re import compile, search

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
                "NL": "Dutch"
}

# TRANSLATIONS.items() returns array of tuples where [0] is key (ISO 639-1 code) and [1] is value (name of language).
# sorted() sorts an array of items based on a key, which in this case is a function which simply returns [1], the value.
# i.e. TRANSLATIONS is now a sorted array of tuples, in ascending alphabetical order on the name of the language.
LANGUAGES = [(key, value) for (key, value) in sorted(LANGUAGES.items(), key=lambda x: x[1])]

LANGUAGE_HEADER_LINE = 2    # 3rd line in the file is where the Language header goes.

# Matches all characters part of the previous credits section.
# Find '[-*] \[coeurGG\]`
#FIND_PREVIOUS_CREDITS =


def get_credits_list(list_of_authors=None):
    if list_of_authors is None:
        list_of_authors = TRANSLATION_CREDITS

    ret = ""
    for author in list_of_authors:
        ret += author.get_markdown_embed() + "\n"

    return ret


def generate_url_to_file(linked_readme_language, this_readme_language="EN"):
    if linked_readme_language == this_readme_language: return "README.md"   # We're already at this file

    return ("translations/" if this_readme_language == "EN" else "../") + \
           ("../" if linked_readme_language == "EN" else linked_readme_language + "/") + \
            "README.md"


def get_readme_header_links(this_readme_language="EN", header_separator=" | "):
    ret = []
    for (iso_code, name) in LANGUAGES:
        if name == this_readme_language:
            ret.append(name)
        else:
            ret.append(generate_url_to_file(iso_code, this_readme_language))

    return header_separator.join(ret)


if __name__ == "__main__":
    # Relative links are in the context of the base directory, which is where the English README file is.
    files = [generate_url_to_file(iso_code, "EN") for (iso_code, name) in LANGUAGES]
    # Read file, overwrite 3rd line (
