"""
Checks for specific programs or services that may conflict with SCBlocker.

Author: Daniel "Speyedr" Summer
"""

from logger import Logger                           # :peepolove:
from psutil import Process, process_iter, AccessDenied, NoSuchProcess
from pygtrie import StringTrie, CharTrie
from re import compile, match, search, MULTILINE

# From https://www.reqrypt.org/windivert.html > Projects
POSSIBLE_CONFLICTS = [
                      "reqrypt",
                      "suricata",
                      "goodbyedpi",
                      "barbatunnel",
                      "streamdivert",
                      "httpfilteringengine",
                      "tallow",
                      "clumsy",
                      "inssidious",
                      "lumogate",
                      "snoopspy3",
                      "mitmproxy",
                      "mitmdump",
                      "mitmweb",
                      "vpnhood",
                      "warp.exe",
                      "warp-svc"
                     ]


WINDIVERT_LIBRARIES = [
                       "windivert",
                       #"windivert32",  # Clever usage of CharTrie means we don't need to check 32 or 64
                       #"windivert64"
                      ]

KNOWN_GOOD_PROCESSES = [
                        "guardian"      # Guardian's filtering methods do not conflict with SCBlocker
                       ]

STRING_SEPARATOR = "\x00"      # process names can't have a null byte in them so will use as separator
PROCESS_SUFFIX = ".exe"        # all process names end in .exe
LIBRARY_SUFFIX = ".dll"        # all dynamic link libraries end in .dll

LOG_FILE = "conflicts.log"     # DEBUG: will be changed to debug.log in production

# Matches the name of a file from a directory path
FILE_GET_NAME = compile("(?<=\\\\)[^\\\\]+$")    # Backslash plague makes me want to cry


def get_all_process_names():
    return [(process.name(), process.pid) for process in process_iter()]


def construct_process_trie():
    """
    In order to efficiently compare several different strings against a large text, I've decided to use a Trie data
    structure. Naive comparisons of two texts against each other are O(m*n^2). Using a Trie structure, we can get this
    down to O(n+m), which scales *much* better when a lot of processes are running.

    :return: a pygtrie.CharTrie containing all process names currently running on the computer.
    """

    trie = CharTrie()
    for (process_name, process_id) in get_all_process_names():
        trie[process_name.lower()] = construct_module_trie(process_id)

    return trie


def construct_module_trie(process_id):
    """
    :param process_id:
    :return: Trie containing all loaded modules in a process.
    """
    trie = CharTrie()
    # FIXME: There seems to be poor performance here somewhere. Investigate the performance of the regex search.
    #  Should maybe switch to a different method of getting the file name, like str.split("\\")?

    try:
        proc = Process(process_id)
    except (AccessDenied, NoSuchProcess) as e:
        Logger.static_add_message("WARNING: Could not open process ID " + str(process_id) +
                                  "\nReason: " + str(e))
        return trie
    # Otherwise, we were able to open the process.

    try:
        for dll in proc.memory_maps():
            filename = search(FILE_GET_NAME, dll.path)
            if filename:
                trie[filename.group().lower()] = dll.rss
    except (AccessDenied, NoSuchProcess) as e:     # Could not open process
        Logger.static_add_message("WARNING: Could not get modules for process ID " + str(process_id) +
                                  "\nReason: " + str(e))

    return trie


def get_conflicts(process_trie=None, process_conflicts=None):
    if process_trie is None:
        process_trie = construct_process_trie()

    if process_conflicts is None:
        process_conflicts = POSSIBLE_CONFLICTS

    library_conflicts = WINDIVERT_LIBRARIES

    conflicts = []

    # STEP 1: Any process names that match conflicting processes.
    for conflict in process_conflicts:
        matches = process_trie.keys(conflict)   # get any process names that match this conflict
        while len(matches) > 0:                 # deplete list of matches
            this_match = matches.pop()
            conflicts.append(this_match)        # add the match to list of conflicts
            del process_trie[this_match]        # remove it from the trie, we already know it's a conflict

    """
    Thinking about this now, if we have step 2, step 1 is _probably_ redundant?
    Will leave both in for now, but like, wouldn't we end up finding those processes from step 1 with step 2 anyways?
    ...unless those processes have statically linked? Will need to test.
    """

    # STEP 2: Any processes that contain conflicting modules.
    for windivert in library_conflicts:
        for process_name, module_trie in process_trie.items():
            matches = module_trie.keys(windivert)
            if len(matches) > 0:                # there are modules in this process that match a conflict
                conflicts.append(process_name)  # append the process. we don't actually care which modules matched
            del process_trie[process_name]      # technically not necessary cause no more processing

    Logger.static_add_message("Conflicts found: " + str(conflicts))
    return conflicts


if __name__ == "__main__":
    proc = get_all_process_names()
    print(proc)
    for pname, pid in proc:
        trie = construct_module_trie(pid)
        print(trie)

