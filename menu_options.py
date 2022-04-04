from colorama import init, Fore, Back   # for colouring boolean options
from translator import Translator, MissingTranslationBehaviour as MTB
from enum import Enum, auto
from logger import Logger
from os import scandir

init()  # initializes colorama library

DEFAULT_LANGUAGE = "EN"
LOG_FILE = "menu.log"   # DEBUG: Will be changed to debug.log in production
TRANSLATION_FOLDER = "translations"


class MenuTypes(Enum):
    MAIN_MENU = 0
    FILTER_SETTINGS_MENU = auto()
    LANGUAGE_SETTINGS_MENU = auto()


def toggle_option(name):
    # There's absolutely a better way to do this but I can't be bothered coming up with it at the moment lol
    if name == MenuText.FILTER: Menu.IS_FILTER_RUNNING = not Menu.IS_FILTER_RUNNING
    if name == MenuText.LOG_BLOCKED_ACTIVITY: Menu.IS_LOGGING = not Menu.IS_LOGGING
    if name == MenuText.DROP_INC_80:
        Menu.IS_DROP_INC_80 = not Menu.IS_DROP_INC_80
        if Menu.DROP_OPTIONS_MUTUALLY_EXCLUSIVE:
            Menu.IS_DROP_CLIENT_POST = False
            Menu.IS_DROP_LENGTH = False
    if name == MenuText.DROP_CLIENT_POST:
        Menu.IS_DROP_CLIENT_POST = not Menu.IS_DROP_CLIENT_POST
        if Menu.DROP_OPTIONS_MUTUALLY_EXCLUSIVE:
            Menu.IS_DROP_INC_80 = False
            Menu.IS_DROP_LENGTH = False
    if name == MenuText.DROP_LENGTHS:
        Menu.IS_DROP_LENGTH = not Menu.IS_DROP_LENGTH
        if Menu.DROP_OPTIONS_MUTUALLY_EXCLUSIVE:
            Menu.IS_DROP_INC_80 = False
            Menu.IS_DROP_CLIENT_POST = False


class MenuText:
    FILTER = Translator("FILTER:", "MenuText_FILTER", "EN", MTB.DEFAULT_TO_ENGLISH)
    ADJUST_FILTER = Translator("ADJUST FILTER SETTINGS", "MenuText_ADJUST_FILER", "EN", MTB.DEFAULT_TO_ENGLISH)
    LOG_BLOCKED_ACTIVITY = Translator("LOG BLOCKED ACTIVITY:", "MenuText_LOG_BLOCKED_ACTIVITY", "EN", MTB.DEFAULT_TO_ENGLISH)
    OPEN_DONATION_URL = Translator("Open Donation URL", "MenuText_OPEN_DONATION_URL", "EN", MTB.DEFAULT_TO_ENGLISH)
    EXIT_PROGRAM = Translator("EXIT PROGRAM", "MenuText_EXIT_PROGRAM", "EN", MTB.DEFAULT_TO_ENGLISH)
    DROP_INC_80 = Translator("DROP INC 80:", "MenuText_DROP_INC_80", "EN", MTB.DEFAULT_TO_ENGLISH)
    DROP_CLIENT_POST = Translator("DROP CLIENT POST [RECOMMENDED]:", "MenuText_DROP_CLIENT_POST", "EN", MTB.DEFAULT_TO_ENGLISH)
    DROP_LENGTHS = Translator("DROP LENGTHS [EXPERIMENTAL]:", "MenuText_DROP_LENGTHS", "EN", MTB.DEFAULT_TO_ENGLISH)
    FILTER_SETTINGS_GO_BACK = Translator("Go back", "MenuText_FILTER_SETTINGS_GO_BACK", "EN", MTB.DEFAULT_TO_ENGLISH)
    CHANGE_LANGUAGE = Translator("CHANGE DISPLAY LANGUAGE", "MenuText_CHANGE_LANGUAGE", "EN", MTB.DEFAULT_TO_ENGLISH)

    STOP = Translator("Stop", "MenuText_STOP", "EN", MTB.DEFAULT_TO_ENGLISH)
    START = Translator("Start", "MenuText_START", "EN", MTB.DEFAULT_TO_ENGLISH)

    ON = Translator("ON", "MenuText_ON", "EN", MTB.DEFAULT_TO_ENGLISH)
    OFF = Translator("OFF", "MenuText_OFF", "EN", MTB.DEFAULT_TO_ENGLISH)

    FILTER_INSTRUCTIONS_1 = Translator("Press 1 to", "MenuText_FILTER_INSTRUCTIONS_1", "EN", MTB.DEFAULT_TO_ENGLISH)
    FILTER_INSTRUCTIONS_2 = Translator("the network filter.", "MenuText_FILTER_INSTRUCTIONS_2", "EN", MTB.DEFAULT_TO_ENGLISH)

    ERR_MSG_NO_FILTERS_1 = Translator("ERROR: Attempted to start the network filter but",
                                      "MenuText_ERR_MSG_NO_FILTERS_1", "EN", MTB.DEFAULT_TO_ENGLISH)
    ERR_MSG_NO_FILTERS_2 = Translator("no filters are enabled", "MenuText_ERR_MSG_NO_FILTERS_2", "EN", MTB.DEFAULT_TO_ENGLISH)
    ERR_MSG_NO_FILTERS_3 = Translator("Press 2", "MenuText_ERR_MSG_NO_FILTERS_3", "EN", MTB.DEFAULT_TO_ENGLISH)
    ERR_MSG_NO_FILTERS_4 = Translator("to open the filter settings and", "MenuText_ERR_MSG_NO_FILTERS_4", "EN", MTB.DEFAULT_TO_ENGLISH)
    ERR_MSG_NO_FILTERS_5 = Translator("enable at least one", "MenuText_ERR_MSG_NO_FILTERS_5", "EN", MTB.DEFAULT_TO_ENGLISH)
    ERR_MSG_NO_FILTERS_6 = Translator("of them!", "MenuText_ERR_MSG_NO_FILTERS_6", "EN", MTB.DEFAULT_TO_ENGLISH)

    WRN_MSG_NO_SERVER_IP = Translator("WARNING: Server IP could not be resolved, using backup filter.\n"
                                      "Performance may be sub-optimal. Restart the filter to try again,\n"
                                      "or Press 2 to open the filter settings and select DROP_INC_80.",
                                      "MenuText_WRN_MSG_NO_SERVER_IP", "EN", MTB.DEFAULT_TO_ENGLISH)

    ADJUST_FILTER_DESC = Translator("Change / update which filters you're currently using.",
                                    "MenuText_ADJUST_FILTER_DESC", "EN", MTB.MISSING_TRANSLATION_TEXT)
    LOG_BLOCKED_ACTIVITY_DESC = Translator("Log information to the debug file about what was blocked and why.",
                                           "MenuText_IS_LOGGING_DESC", "EN", MTB.MISSING_TRANSLATION_TEXT)
    CHANGE_LANGUAGE_DESC = Translator("Change the language of the menus.",
                                      "MenuText_CHANGE_LANGUAGE_DESC", "EN", MTB.MISSING_TRANSLATION_TEXT)
    EXIT_PROGRAM_DESC = Translator("Safely exit the program.", "MenuText_EXIT_PROGRAM_DESC", "EN", MTB.MISSING_TRANSLATION_TEXT)
    FILTER_SETTINGS_GO_BACK_DESC = Translator("Save your changes and go back to the main menu.",
                                              "MenuText_FILTER_SETTINGS_GO_BACK_DESC", "EN", MTB.MISSING_TRANSLATION_TEXT)

    DROP_INC_80_EXPLANATION = Translator(
                                    "In order to notify your client of an incoming notification, R* Servers\n"
                                    "will send you a specific packet. Dropping this packet will prevent your client\n"
                                    "from being made aware of new notifications entirely. This method is fast and\n"
                                    "simple but may conflict with in-game traffic, and you may be flooded with\n"
                                    "notifications when the filter is turned off.",
                                    "MenuText_DROP_INC_80_EXPLANATION", "EN", MTB.MISSING_TRANSLATION_TEXT)
    DROP_CLIENT_POST_EXPLANATION = Translator(
                                    "If your client is informed that it has notifications to fetch\n"
                                    "(i.e. DROP INC 80 is OFF), your client will POST some data to a specific endpoint.\n"
                                    "Enabling this setting will drop packets that are sent to this endpoint.\n"
                                    "Much less likely to interfere with in-game traffic, but computationally\n"
                                    "expensive and will block all notifications.",
                                    "MenuText_DROP_CLIENT_POST_EXPLANATION", "EN", MTB.MISSING_TRANSLATION_TEXT)
    DROP_LENGTHS_EXPLANATION = Translator(
                                    "All payloads sent and received when playing GTA Online are encrypted, but\n"
                                    "uncompressed. This means that even if we can't see the packet's details, we can\n"
                                    "\"guess\" what type it is based on its' size. This method is surprisingly powerful\n"
                                    "and can allow some notifications through while still blocking session invites.\n"
                                    "However, this filter is a work in progress and may not behave correctly.",
                                    "MenuText_DROP_LENGTHS_EXPLANATION", "EN", MTB.MISSING_TRANSLATION_TEXT)

    @staticmethod
    def update_language(language):
        for attr_name, translator_object in vars(MenuText):
            if isinstance(translator_object, Translator):
                translator_object.set_language(language)
            else:
                Logger.static_add_message("[WARNING]: MenuText." + str(attr_name) +
                                          " is not an instance of Translator.", LOG_FILE)


class Menu:
    IS_FILTER_RUNNING = True
    START_STOP_STR = "Stop" if IS_FILTER_RUNNING else "Start"
    IS_LOGGING = False

    IS_DROP_INC_80 = False
    IS_DROP_CLIENT_POST = True
    IS_DROP_LENGTH = False

    DROP_OPTIONS_MUTUALLY_EXCLUSIVE = True  # Can't have more than one drop option enabled at a time.

    DISPLAY_LANGUAGE = DEFAULT_LANGUAGE

    ERR_MSG_NO_FILTERS = "\n ERROR: Attempted to start the network filter but "+\
                         Back.RED+"no filters are enabled"+Back.RESET+".\n        "+\
                         Fore.LIGHTCYAN_EX+"Press 2"+Fore.RESET+" to open the filter settings and "+\
                         Fore.LIGHTCYAN_EX+"enable at least one"+Fore.RESET+" of them!"

    WRN_MSG_NO_SERVER_IP = "\n WARNING: Server IP could not be resolved, using backup filter.\n"+\
                           "Performance may be sub-optimal. Restart the filter to try again,\n"+\
                           "or Press 2 to open the filter settings and select DROP_INC_80."

    """
    Key is text to change option.
    """
    MAIN_OPTIONS = {"1": {"value": IS_FILTER_RUNNING,
                          "name": MenuText.FILTER.get_message("EN"),
                          "visual_name": MenuText.FILTER.get_message(),
                          "desc": "Press 1 to "+START_STOP_STR+" the network filter.",
                          "action": toggle_option},
                    "2": {"value": "",
                          "name": MenuText.ADJUST_FILTER.get_message("EN"),
                          "visual_name": MenuText.FILTER.get_message(),
                          "desc": "Change / update which filters you're currently using."},
                    "3": {"value": IS_LOGGING,
                          "name": MenuText.LOG_BLOCKED_ACTIVITY.get_message("EN"),
                          "visual_name": MenuText.FILTER.get_message(),
                          "desc": "Log information to the debug file about what was blocked and why.",
                          "action": toggle_option},
                    "4": {"value": "",
                          "name": MenuText.CHANGE_LANGUAGE.get_message("EN"),
                          "visual_name": MenuText.FILTER.get_message(),
                          "desc": "Change the language of the menus."},
                    "5": {"value": "",
                          "name": MenuText.OPEN_DONATION_URL.get_message("EN"),
                          "visual_name": MenuText.FILTER.get_message(),
                          "desc": "If this program helped you, donating would be a great way of saying thanks."},
                    "x": {"value": "",
                          "name": MenuText.EXIT_PROGRAM.get_message("EN"),
                          "visual_name": MenuText.FILTER.get_message(),
                          "desc": "Safely exit the program."}}

    FILTER_OPTIONS = {"1": {"value": IS_DROP_INC_80,
                            "name": MenuText.DROP_INC_80.get_message("EN"),
                            "visual_name": MenuText.FILTER.get_message(DISPLAY_LANGUAGE),
                            "desc": "In order to notify your client of an incoming notification, R* Servers\n"
                                    "will send you a specific packet. Dropping this packet will prevent your client\n"
                                    "from being made aware of new notifications entirely. This method is fast and\n"
                                    "simple but may conflict with in-game traffic, and you may be flooded with\n"
                                    "notifications when the filter is turned off.",
                                    "action": toggle_option},
                      "2": {"value": IS_DROP_CLIENT_POST,
                            "name": MenuText.DROP_CLIENT_POST.get_message("EN"),
                            "visual_name": MenuText.FILTER.get_message(DISPLAY_LANGUAGE),
                            "desc": "If your client is informed that it has notifications to fetch\n"
                                    "(i.e. DROP INC 80 is OFF), your client will POST some data to a specific endpoint.\n"
                                    "Enabling this setting will drop packets that are sent to this endpoint.\n"
                                    "Much less likely to interfere with in-game traffic, but computationally\n"
                                    "expensive and will block all notifications.",
                                    "action": toggle_option},
                      "3": {"value": IS_DROP_LENGTH,
                            "name": MenuText.DROP_LENGTHS.get_message("EN"),
                            "visual_name": MenuText.FILTER.get_message(DISPLAY_LANGUAGE),
                            "desc": "All payloads sent and received when playing GTA Online are encrypted, but\n"
                                    "uncompressed. This means that even if we can't see the packet's details, we can\n"
                                    "\"guess\" what type it is based on its' size. This method is surprisingly powerful\n"
                                    "and can allow some notifications through while still blocking session invites.\n"
                                    "However, this filter is a work in progress and may not behave correctly.",
                                    "action": toggle_option},
                      "b": {"value": "",
                            "name": MenuText.FILTER_SETTINGS_GO_BACK.get_message("EN"),
                            "visual_name": MenuText.FILTER.get_message(DISPLAY_LANGUAGE),
                            "desc": "Save your changes and go back to the main menu."}}

    @staticmethod
    def construct_print_options(options):
        ret = ""                    # I'm aware of the O(n^2) complexity of this function. Please don't hurt me.
        for key in options:
            ret += " " + key + ") " + options[key]["name"] + " " + Menu.color_bool(options[key]["value"]) + "\n" +\
                   "\t" + options[key]["desc"].replace("\n", "\n\t") + "\n\n"
        return ret

    @staticmethod
    def generate_main_menu():
        return {"1": {"value": Menu.IS_FILTER_RUNNING,
                      "name": MenuText.FILTER.get_message("EN"),
                      "visual_name": MenuText.FILTER.get_message(),
                      "desc": Menu.filter_instructions(),
                      "action": toggle_option},

                "2": {"value": "",
                      "name": MenuText.ADJUST_FILTER.get_message("EN"),
                      "visual_name": MenuText.ADJUST_FILTER.get_message(),
                      "desc": MenuText.ADJUST_FILTER_DESC.get_message()},

                "3": {"value": Menu.IS_LOGGING,
                      "name": MenuText.LOG_BLOCKED_ACTIVITY.get_message("EN"),
                      "visual_name": MenuText.LOG_BLOCKED_ACTIVITY.get_message(),
                      "desc": MenuText.LOG_BLOCKED_ACTIVITY_DESC.get_message(),
                      "action": toggle_option},

                "4": {"value": "",
                      "name": MenuText.CHANGE_LANGUAGE.get_message("EN"),
                      "visual_name": MenuText.CHANGE_LANGUAGE.get_message(),
                      "desc": MenuText.CHANGE_LANGUAGE_DESC.get_message()},

                "5": {"value": "",
                      "name": MenuText.OPEN_DONATION_URL.get_message("EN"),
                      "visual_name": MenuText.OPEN_DONATION_URL.get_message(),
                      "desc": "If this program helped you, donating would be a great way of saying thanks."},

                "x": {"value": "",
                      "name": MenuText.EXIT_PROGRAM.get_message("EN"),
                      "visual_name": MenuText.EXIT_PROGRAM.get_message(),
                      "desc": MenuText.EXIT_PROGRAM_DESC.get_message()}}

    @staticmethod
    def generate_filter_settings_menu():
        return   {"1": {"value": Menu.IS_DROP_INC_80,
                        "name": MenuText.DROP_INC_80.get_message("EN"),
                        "visual_name": MenuText.DROP_INC_80.get_message(),
                        "desc": MenuText.DROP_INC_80_EXPLANATION.get_message(),
                        "action": toggle_option},

                  "2": {"value": Menu.IS_DROP_CLIENT_POST,
                        "name": MenuText.DROP_CLIENT_POST.get_message("EN"),
                        "visual_name": MenuText.DROP_CLIENT_POST.get_message(),
                        "desc": MenuText.DROP_CLIENT_POST_EXPLANATION.get_message(),
                        "action": toggle_option},

                  "3": {"value": Menu.IS_DROP_LENGTH,
                        "name": MenuText.DROP_LENGTHS.get_message("EN"),
                        "visual_name": MenuText.DROP_LENGTHS.get_message(),
                        "desc": MenuText.DROP_LENGTHS_EXPLANATION.get_message(),
                        "action": toggle_option},

                  "b": {"value": "",
                        "name": MenuText.FILTER_SETTINGS_GO_BACK.get_message("EN"),
                        "visual_name": MenuText.FILTER_SETTINGS_GO_BACK.get_message(),
                        "desc": MenuText.FILTER_SETTINGS_GO_BACK_DESC.get_message()}}

    @staticmethod
    def generate_language_settings_menu(page=0, max_entries_per_page=9):
        # Check the translations folder, get sub-folders, check Author's file.
        start_key = "1"
        has_prev_page = page > 0
        lang_codes = [file.path[len(TRANSLATION_FOLDER)+1:] for file in scandir(TRANSLATION_FOLDER) if file.is_dir()]
        has_next_page = (page+1) * max_entries_per_page < len(lang_codes)

        try:
            lang_codes = lang_codes[page*max_entries_per_page:]     # trim from left
        except IndexError as e:
            raise e     # no handling yet. essentially, this error occurs when a page cannot exist / is empty

        lang_codes = lang_codes[:max_entries_per_page]  # this should never fail; it's like minimising on a maximum

        return ""

    @staticmethod
    def generate_menu(menu_type):
        if menu_type == MenuTypes.MAIN_MENU:
            return Menu.generate_main_menu()
        if menu_type == MenuTypes.FILTER_SETTINGS_MENU:
            return Menu.generate_filter_settings_menu()
        if menu_type == MenuTypes.LANGUAGE_SETTINGS_MENU:
            return Menu.generate_language_settings_menu()

    @staticmethod
    def construct_menu(menu_type):
        return Menu.construct_print_options(Menu.generate_menu(menu_type))

    @staticmethod
    def update_menu():
        Menu.MAIN_OPTIONS["1"]["value"]   = Menu.IS_FILTER_RUNNING
        Menu.MAIN_OPTIONS["1"]["desc"]    = Menu.filter_instructions()
        Menu.MAIN_OPTIONS["3"]["value"]   = Menu.IS_LOGGING
        Menu.FILTER_OPTIONS["1"]["value"] = Menu.IS_DROP_INC_80
        Menu.FILTER_OPTIONS["2"]["value"] = Menu.IS_DROP_CLIENT_POST
        Menu.FILTER_OPTIONS["3"]["value"] = Menu.IS_DROP_LENGTH

    @staticmethod
    def filter_instructions():
        return "Press 1 to "+(Fore.RED+"Stop" if Menu.IS_FILTER_RUNNING else Fore.CYAN+"Start")+Fore.RESET\
               +" the network filter."

    @staticmethod
    def color_bool(boolean, color_true=Fore.LIGHTGREEN_EX, color_false=Fore.GREEN):
        if not isinstance(boolean, bool): return boolean
        return (color_true + "ON" if boolean else color_false + "OFF") + Fore.RESET

    @staticmethod
    def get_options():
        return Menu.IS_FILTER_RUNNING, Menu.IS_LOGGING, Menu.IS_DROP_INC_80, Menu.IS_DROP_CLIENT_POST, \
               Menu.IS_DROP_LENGTH, Menu.DISPLAY_LANGUAGE

    @staticmethod
    def set_options(options):
        version_number = 0
        try:
            version_number = int(options[0])
        except ValueError:
            pass    # assume version 0 (which didn't have a version number)
        else:
            options = options[1:]   # remove the version number (it's not a setting)

        if version_number >= 0:
            Menu.IS_FILTER_RUNNING = options[0]
            Menu.IS_LOGGING = options[1]
            Menu.IS_DROP_INC_80 = options[2]
            Menu.IS_DROP_CLIENT_POST = options[3]
            Menu.IS_DROP_LENGTH = options[4]
        if version_number >= 1:
            Menu.DISPLAY_LANGUAGE = options[5]

    @staticmethod
    def emphasize():
        Menu.MAIN_OPTIONS["4"]["desc"] = Fore.WHITE + Menu.MAIN_OPTIONS["4"]["desc"] + Fore.RESET
