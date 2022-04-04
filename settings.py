
conversion_map = {"True": True,
                  "False": False,
                  "None": None}


def convert(item):
    try:
        return conversion_map[item]
    except KeyError:
        pass

    try:
        return int(item)
    except ValueError:
        pass

    try:
        return float(item)
    except ValueError:
        pass

    return item


class Settings:
    CURRENT_VERSION_NUMBER = 1

    def __init__(self, default_settings, file_location="config.ini"):
        self.file_location = file_location
        try:
            self.get_settings()
        except FileNotFoundError:
            self.write_settings(default_settings)

    def get_settings(self):
        handle = open(self.file_location, "r")
        content = handle.read()
        handle.close()
        return [convert(i) for i in content.split('\n')]      # every element is a different line

    def write_settings(self, elements_to_save):
        all_strings = [str(Settings.CURRENT_VERSION_NUMBER)] + [str(i) for i in elements_to_save]
        overwrite = '\n'.join(all_strings)
        handle = open(self.file_location, "w")
        handle.write(overwrite)
        handle.close()
