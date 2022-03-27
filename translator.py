"""
Dynamic file implementation for translating descriptions and messages within the program.

Author: Daniel "Speyedr" Summer

The goal of this Translator class is to be easily readable and usable by developers, code reviewers and end users.
I don't want this class to be so abstract and dynamic that it's impossible to understand or read messages from just
looking at the code, and I also want to make translation accessible and dynamic so that anyone can provide translations
without having to modify or update the program or conform to any programming syntax.
"""

from enum import Enum, auto
from logger import Logger

from main import LOG_FILE

TRANSLATION_FILE_MARKER = "# TRANSLATION_BEGIN:"
NO_TRANSLATION = "[Missing Translation]"


class MissingTranslation(Exception):
    """ A translation for this message in the specified language does not exist. """
    pass


class MissingTranslationBehaviour(Enum):
    RAISE_EXCEPTION = auto()
    DEFAULT_TO_ENGLISH = auto()
    MISSING_TRANSLATION_TEXT = auto()


class Translator:
    """
    The Translator class allows messages to be constructed using a specific language, and then "swapped out" by loading
    an alternative message from a file located at `translations\\[LANGUAGE]\\location`.txt.
    For example, a Translator object could be
    initialized as: `Translator("This is a test message", "TEST_MESSAGE", "EN")`.
    Returning the message in the current language that is set is done with .get_message().
    Alternatively, this can be temporarily overridden by supplying .get_message() with a parameter for the language.
    The method .set_language("FR") can be called, at which point the file at
    `translations\\FR\\TEST_MESSAGE.TXT` is read, and
    any further calls to .get_message() will default to the French translation.
    """

    def __init__(self, message, location, language="EN",
                 no_translation=MissingTranslationBehaviour.MISSING_TRANSLATION_TEXT):
        self.translations = {language: message}
        self.location = location
        self.current_language = language
        self.error_behaviour = None
        self.set_missing_translation_behaviour(no_translation)

    def get_message(self, language=None):
        if language is None:
            language = self.current_language

        try:
            return self.translations[language]      # Return message in the specified language.
        except KeyError:
            try:
                return self.load_message(language)             # If no translation, attempt to load one from file.
            except MissingTranslation as e:
                Logger.static_add_message(str(e), LOG_FILE)
                if self.error_behaviour == MissingTranslationBehaviour.RAISE_EXCEPTION:
                    raise MissingTranslation("A '" + language + "' translation for this message does not exist.")
                if self.error_behaviour == MissingTranslationBehaviour.DEFAULT_TO_ENGLISH:
                    return self.get_message("EN")
                if self.error_behaviour == MissingTranslationBehaviour.MISSING_TRANSLATION_TEXT:
                    return NO_TRANSLATION
                assert False, "Undefined Missing Translation Behaviour: " + str(self.error_behaviour)

    def set_language(self, language):
        """
        Sets the current language if and only if a translation for this message in `language` is already saved, or,
        is successfully loaded from a translation file. If a translation for this message in `language` cannot be found,
        a MissingTranslation exception will occur.
        :param language: Language to change to
        :return:
        """
        self.get_message(language)
        self.current_language = language    # If we reached here, then a translation exists.

    def load_message(self, language):
        handle = None
        try:
            handle = open("translations\\" + language + "\\" + self.location + ".txt")
        except (FileNotFoundError, PermissionError) as e:
            if isinstance(e, FileNotFoundError):
                raise MissingTranslation("Could not load a '" + language + "' translation for this message: "
                                         "File does not exist / could not be found.")
            if isinstance(e, PermissionError):
                raise MissingTranslation("Could not load a '" + language + "' translation for this message: "
                                         "Access is denied.")
        # Not sure if there's other I/O errors I should be handling
        assert handle is not None, "File did not open successfully but exception was not caught."

        lines = handle.readlines()
        # Find where translation begins (# TRANSLATION_BEGIN:)
        i = 0
        while i < len(lines):
            if lines[i].find(TRANSLATION_FILE_MARKER) != -1:
                break   # found translation marker
            i += 1      # keep searching

        if i == len(lines):         # reached end of file, no marker
            raise MissingTranslation("Could not find a '" + language + "' translation for this message:"
                                     "File exists, but translation marker " + TRANSLATION_FILE_MARKER +
                                     "was not found.")

        if i == len(lines)-1:       # found marker, but there's no content after it
            raise MissingTranslation("Could not find a '" + language + "' translation for this message:"
                                     "Translation marker found, but there isn't any content to save underneath it.")

        # else, everything from i+1 to end is the translated message
        message = "\n".join(lines[i+1:])
        self.save_translation(message, language)    # save the translation so it can be easily accessed next time
        return message

    def save_translation(self, message, language):
        self.translations[language] = message

    def set_missing_translation_behaviour(self, behaviour):
        if not isinstance(behaviour, MissingTranslationBehaviour):
            raise ValueError("Unsupported translation behaviour: " + str(behaviour))
        self.error_behaviour = behaviour


if __name__ == "__main__":
    tr = Translator("This is a test message.", "tr_test", "EN", MissingTranslationBehaviour.MISSING_TRANSLATION_TEXT)
    print(tr.get_message())
    print(tr.translations)
    print(tr.get_message("ES"))
    print(tr.translations)
    tr.set_language("ES")
    print(tr.get_message("EN"))
    print(tr.get_message(""))   # Error handling test
    print(tr.translations)      # Make sure that the erroneous behaviour didn't affect internal structure.
