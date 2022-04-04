"""
Dynamic file implementation for translating descriptions and messages within the program.

Author: Daniel "Speyedr" Summer

The goal of this Translator class is to be easily readable and usable by developers, code reviewers and end users.
I don't want this class to be so abstract that it's impossible to understand or read messages from just
looking at the code, but I also want to make translation accessible and dynamic so that anyone can provide translations
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


class TranslatorManager:

    saved_translations = {}

    @staticmethod
    def add_translation(message, location, language):
        TranslatorManager.saved_translations[(location, language)] = message

    @staticmethod
    def get_translation(location, language):
        return TranslatorManager.saved_translations[(location, language)]


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
    override_translation
    """

    def __init__(self, message, location, language="EN",
                 no_translation=MissingTranslationBehaviour.MISSING_TRANSLATION_TEXT,
                 write_translation=True, override_translation=True):
        self.translations = {language: message}
        self.location = location
        self.current_language = language
        self.error_behaviour = None
        self.set_missing_translation_behaviour(no_translation)
        self.should_write = write_translation
        self.should_override = override_translation

        if self.should_write:
            self.write_translation()

        TranslatorManager.add_translation(message, location, language)
        return

    def __str__(self):
        return self.get_message(self.current_language)

    def get_message(self, language=None, error_behaviour=None):
        if language is None:
            language = self.current_language

        if error_behaviour is None:
            error_behaviour = self.error_behaviour

        try:
            return self.translations[language]      # Return message in the specified language.
        except KeyError:
            try:
                return self.load_message(language)             # If no translation, attempt to load one from file.
            except MissingTranslation as e:
                Logger.static_add_message(str(e), LOG_FILE)
                if error_behaviour == MissingTranslationBehaviour.RAISE_EXCEPTION:
                    raise MissingTranslation("A '" + language + "' translation for this message does not exist.")
                if error_behaviour == MissingTranslationBehaviour.DEFAULT_TO_ENGLISH:
                    # Make sure to not infinitely recurse in case an English translation never existed
                    return self.get_message("EN", MissingTranslationBehaviour.MISSING_TRANSLATION_TEXT)
                if error_behaviour == MissingTranslationBehaviour.MISSING_TRANSLATION_TEXT:
                    return NO_TRANSLATION
                assert False, "Undefined Missing Translation Behaviour: " + str(error_behaviour)

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

    def load_message(self, language, force_load_from_file=False):
        if not force_load_from_file:
            try:
                return TranslatorManager.get_translation(self.location, language)
            except KeyError:
                pass

        handle = None
        try:
            handle = open(self.get_file_location(language))
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
        i = self.find_translation_marker(lines, language)

        # else, everything from i+1 to end is the translated message
        message = "\n".join(lines[i+1:])
        self.save_translation(message, language)    # save the translation so it can be easily accessed next time
        return message

    def save_translation(self, message, language):
        TranslatorManager.add_translation(message, self.location, language)
        self.translations[language] = message

    def write_translation(self, language=None):
        if language is None:
            language = self.current_language

        handle = None
        flag = "r" if self.should_override else "x"
        lines = []
        try:
            handle = open(self.get_file_location(language), flag)
        except (FileExistsError, PermissionError) as e:
            raise e     # we currently have no custom behaviour handler for this
        except FileNotFoundError:
            pass        # no need to do all the extra work to create and read a file that doesn't exist
        else:
            lines = handle.readlines()
            handle.close()  # let's be good developers and not leak handles

        # find the marker (so we can overwrite everything after it)
        marker_position = self.find_translation_marker(lines, language, False, False)
        if marker_position >= len(lines):   # no marker was found
            lines.append(TRANSLATION_FILE_MARKER+'\n')   # create a marker

        # now, we remove everything after the marker
        lines = lines[:marker_position+1]
        message = self.get_message(language).splitlines(True)    # get the message we should be writing
        lines.extend(message)   # put the message at the end

        # time to actually save
        flag = "w+"  # we'll be overriding this time
        try:
            handle = open(self.get_file_location(language), flag)
        except PermissionError as e:
            raise e  # we currently have no custom behaviour handler for this

        handle.write("".join(lines))
        handle.close()
        return

    def get_file_location(self, language):
        return "translations\\" + language + "\\" + self.location + ".txt"

    def find_translation_marker(self, content_lines, language="", require_marker=True, require_translation=True):
        # Find where translation begins (# TRANSLATION_BEGIN:)
        i = 0
        while i < len(content_lines):
            if content_lines[i].find(TRANSLATION_FILE_MARKER) != -1:
                break  # found translation marker
            i += 1  # keep searching

        if i == len(content_lines) and require_marker:  # reached end of file, no marker
            raise MissingTranslation("Could not find a '" + language + "' translation for this message:"
                                                                       "File exists, but translation marker " + TRANSLATION_FILE_MARKER +
                                     "was not found.")

        if i == len(content_lines) - 1 and require_translation:  # found marker, but there's no content after it
            raise MissingTranslation("Could not find a '" + language + "' translation for this message:"
                                                                       "Translation marker found, but there isn't any content to save underneath it.")

        return i

    def set_missing_translation_behaviour(self, behaviour):
        if not isinstance(behaviour, MissingTranslationBehaviour):
            raise ValueError("Unsupported translation behaviour: " + str(behaviour))
        self.error_behaviour = behaviour


if __name__ == "__main__":
    tr = Translator("This is a secondary test message.", "tr_test", "EN", MissingTranslationBehaviour.MISSING_TRANSLATION_TEXT, True)
    print(tr.get_message())
    print(tr.translations)
    print(tr.get_message("ES"))
    print(tr.translations)
    tr.set_language("ES")
    print(tr.get_message("EN"))
    print(tr.get_message(""))   # Error handling test
    print(tr.translations)      # Make sure that the erroneous behaviour didn't affect internal structure.
    Translator("This is a new test message.", "tr_test_new", "EN", MissingTranslationBehaviour.RAISE_EXCEPTION, True)
    tr2 = Translator("Este es un nuevo mensaje de prueba.", "tr_test_new", "ES", MissingTranslationBehaviour.RAISE_EXCEPTION, True)
    tr2.set_language("EN")
    print(tr2.translations)
