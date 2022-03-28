"""
Checks for specific programs or services that may conflict with SCBlocker.

Author: Daniel "Speyedr" Summer
"""
import ctypes
import multiprocessing

from ctypes import windll, wintypes, byref

from logger import Logger                           # :peepolove:
from psutil import Process, process_iter, AccessDenied, NoSuchProcess
from pygtrie import StringTrie, CharTrie
from re import compile, match, search, MULTILINE
from multiprocessing import Queue, freeze_support
from time import perf_counter

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
logger_queue = Queue()

# Matches the name of a file from a directory path
FILE_GET_NAME = compile("(?<=\\\\)[^\\\\]+$")    # Backslash plague makes me want to cry
def file_get_name(string):
    return string.rpartition("\\")[2]   # 3rd element is everything right of the first backslash


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


def construct_module_trie():
    """
    :param process_id:
    :return: Trie containing all loaded modules in a process.
    """
    perf = []
    tries = []
    # FIXME: There seems to be poor performance here somewhere. Investigate the performance of the regex search.
    #  Should maybe switch to a different method of getting the file name, like str.split("\\")?
    open_proc_start = perf_counter()
    log_start = 0
    log_finish = 0
    open_dll_start = 0
    open_dll_finish = 0
    regex_start = 0
    regex_finish = 0
    for proc in process_iter():
        try:
            #proc = Process(process_id)
            open_proc_finish = perf_counter()
        except (AccessDenied, NoSuchProcess) as e:
            log_start = perf_counter()
            logger_queue.put("WARNING: Could not open process ID " + str(proc.pid) +
                                      "\nReason: " + str(e))
            log_finish = perf_counter()
            open_proc_finish = perf_counter()
            perf.extend([open_proc_finish - open_proc_start, log_finish - log_start])
            logger_queue.put(perf)
            continue
        # Otherwise, we were able to open the process.

        try:
            trie = CharTrie()
            open_dll_start = perf_counter()
            for dll in proc.memory_maps():
                #filename = search(FILE_GET_NAME, dll.path)
                #if filename:
                filename = file_get_name(dll.path)
                trie[filename.lower()] = dll.rss
            tries.append(trie)
            open_dll_finish = perf_counter()
        except (AccessDenied, NoSuchProcess) as e:     # Could not open process
            log_start = perf_counter()
            open_dll_start = 0
            logger_queue.put("WARNING: Could not get modules for process ID " + str(proc.pid) +
                                      "\nReason: " + str(e))
            log_finish = perf_counter()

        #open_proc_finish = perf_counter()
        perf.extend([open_proc_finish - open_proc_start, log_finish - log_start,
                     open_dll_finish - open_dll_start])
        logger_queue.put(perf)
    return tries


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

"""
if __name__ == "__main__":
    #process_iter()  # pre-cache
    #freeze_support()
    start = perf_counter()
    logger = Logger(logger_queue, LOG_FILE)
    logger.start()
    one = perf_counter()
    #proc = get_all_process_names()
    print(perf_counter() - one)
    #print(proc)
    #for pname, pid in proc:
    trie = construct_module_trie()
    #print(trie)
    finish = perf_counter()
    print(finish - start)
    logger_queue.put(finish - start)

    # with regex...
    # get_all_process_names(): 0.54799 (seconds?)
    # total: 1.6638957 (seconds?)

    # without regex...
    # get_all_process_names(): 0.6590995 (seconds?)
    # total: 2.07030996 (bruh)

    # regex seems to be slightly faster

    # home PC, regex:
    # 0.08537806800000003, 1.2365573250000002

    # home PC, embedded process_iter(), regex:
    # 0.084129602, 1.170932615

    # home PC, embedded process_iter(), no regex:
    # 0.08495782599999999, 1.115807105"""

if __name__ == "__main__":
    #windll.psapi.EnumProcesses()

    max_processes = 8192
    pids = (wintypes.DWORD * max_processes)()
    pids_size = ctypes.sizeof(pids)
    bytes_returned = wintypes.DWORD()
    success = windll.psapi.EnumProcesses(byref(pids), pids_size, byref(bytes_returned))
    print(bytes_returned.value//ctypes.sizeof(wintypes.DWORD))
    pids = pids[10:bytes_returned.value//ctypes.sizeof(wintypes.DWORD)]
    print(success)
    print(pids)

    PROCESS_QUERY_INFORMATION = 0x0400
    #PROCESS_QUERY_LIMITED_INFORMATION = 0x1000     # I'm not looking to do anything other than view information
    MAX_PATH = 260

    for pid in pids:
        handle_modules = (wintypes.HMODULE * 8192)()
        #handle_process = wintypes.HANDLE
        print(pid)

        handle_process = windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)
        print("handle_process: ", handle_process)
        #print(handle_process.value)
        if handle_process > 0:
            bytes_returned_2 = wintypes.DWORD()

            success = windll.psapi.EnumProcessModules(handle_process, byref(handle_modules),
                                                      ctypes.sizeof(handle_modules), byref(bytes_returned_2))
            print("success: ", success, " | bytes returned: ", bytes_returned.value)
            if success == 0:
                print("error: ", windll.kernel32.GetLastError())
            else:
                print(handle_modules)
                for h_mod in handle_modules:
                    print(h_mod)
                    module_name = (ctypes.c_char * MAX_PATH)()
                    windll.kernel32.GetModuleFileNameA(h_mod, byref(module_name),
                                                       ctypes.sizeof(module_name) // ctypes.sizeof(ctypes.c_char))
                    print(module_name.value)
            #windll.kernel32.CloseHandle(handle_process)


    #for idk in pids:
        #print(idk)
