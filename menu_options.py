from colorama import init, Fore, Back   # for colouring boolean options
from translator import Translator
init()  # initializes colorama library

DEFAULT_LANGUAGE = "EN"


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
    FILTER = Translator("FILTER:", "MenuNames_FILTER", "EN")
    ADJUST_FILTER = Translator("ADJUST FILTER SETTINGS", "MenuNames_ADJUST_FILER", "EN")
    LOG_BLOCKED_ACTIVITY = Translator("LOG BLOCKED ACTIVITY:", "MenuNames_LOG_BLOCKED_ACTIVITY", "EN")
    OPEN_DONATION_URL = Translator("Open Donation URL", "MenuNames_OPEN_DONATION_URL", "EN")
    EXIT_PROGRAM = Translator("EXIT PROGRAM", "MenuNames_EXIT_PROGRAM", "EN")
    DROP_INC_80 = Translator("DROP INC 80:", "MenuNames_DROP_INC_80", "EN")
    DROP_CLIENT_POST = Translator("DROP CLIENT POST [RECOMMENDED]:", "MenuNames_DROP_CLIENT_POST", "EN")
    DROP_LENGTHS = Translator("DROP LENGTHS [EXPERIMENTAL]:", "MenuNames_DROP_LENGTHS", "EN")
    FILTER_SETTINGS_GO_BACK = Translator("Go back", "MenuNames_FILTER_SETTINGS_GO_BACK", "EN")
    CHANGE_LANGUAGE = Translator("CHANGE DISPLAY LANGUAGE", "MenuNames_CHANGE_LANGUAGE", "EN")

    STOP = ""
    START = ""

    ERR_MSG_NO_FILTERS_1 = ""
    ERR_MSG_NO_FILTERS_2 = ""
    ERR_MSG_NO_FILTERS_3 = ""
    ERR_MSG_NO_FILTERS_4 = ""
    ERR_MSG_NO_FILTERS_5 = ""
    ERR_MSG_NO_FILTERS_6 = ""

    WRN_MSG_NO_SERVER_IP = ""

    ADJUST_FILTER_DESC = ""
    IS_LOGGING_DESC = ""
    CHANGE_LANGUAGE_DESC = ""
    EXIT_PROGRAM_DESC = ""
    FILTER_SETTINGS_GO_BACK_DESC = ""

    DROP_INC_80_EXPLANATION = ""
    DROP_CLIENT_POST_EXPLANATION = ""
    DROP_LENGTHS_EXPLANATION = ""

    @staticmethod
    def update_language(language):
        for translator_object in vars(MenuText).values():
            translator_object.set_language(language)

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
                          "visual_name": MenuText.FILTER.get_message(DISPLAY_LANGUAGE),
                          "desc": "Press 1 to "+START_STOP_STR+" the network filter.",
                          "action": toggle_option},
                    "2": {"value": "",
                          "name": MenuText.ADJUST_FILTER.get_message("EN"),
                          "visual_name": MenuText.FILTER.get_message(DISPLAY_LANGUAGE),
                          "desc": "Change / update which filters you're currently using.",},
                    "3": {"value": IS_LOGGING,
                          "name": MenuText.LOG_BLOCKED_ACTIVITY.get_message("EN"),
                          "visual_name": MenuText.FILTER.get_message(DISPLAY_LANGUAGE),
                          "desc": "Log information to the debug file about what was blocked and why.",
                          "action": toggle_option},
                    "4": {"value": "",
                          "name": MenuText.CHANGE_LANGUAGE.get_message("EN"),
                          "visual_name": MenuText.FILTER.get_message(DISPLAY_LANGUAGE),
                          "desc": "Change the language of the menus."},
                    "5": {"value": "",
                          "name": MenuText.OPEN_DONATION_URL.get_message("EN"),
                          "visual_name": MenuText.FILTER.get_message(DISPLAY_LANGUAGE),
                          "desc": "If this program helped you, donating would be a great way of saying thanks."},
                    "x": {"value": "",
                          "name": MenuText.EXIT_PROGRAM.get_message("EN"),
                          "visual_name": MenuText.FILTER.get_message(DISPLAY_LANGUAGE),
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
    def update_menu():
        Menu.MAIN_OPTIONS["1"]["value"]   = Menu.IS_FILTER_RUNNING
        Menu.MAIN_OPTIONS["1"]["desc"]    = Menu.filter_instructions()
        Menu.MAIN_OPTIONS["3"]["value"]   = Menu.IS_LOGGING
        Menu.FILTER_OPTIONS["1"]["value"] = Menu.IS_DROP_INC_80
        Menu.FILTER_OPTIONS["2"]["value"] = Menu.IS_DROP_CLIENT_POST
        Menu.FILTER_OPTIONS["3"]["value"] = Menu.IS_DROP_LENGTH

    @staticmethod
    def generate_language_menu():
        # Check the translations folder, get sub-folders, check Author's file.
        return ""

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
