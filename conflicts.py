"""
Checks for specific programs or services that may conflict with SCBlocker.

Author: Daniel "Speyedr" Summer
"""

from psutil import process_iter
from pygtrie import StringTrie

# From https://www.reqrypt.org/windivert.html > Projects
POSSIBLE_CONFLICTS = ["reqrypt"
                      "suricata"
                      "goodbyedpi"
                      "barbatunnel"
                      "streamdivert"
                      "httpfilteringengine"
                      "tallow"
                      "clumsy"
                      "inssidious"
                      "lumogate.v1.0.1"
                      "snoopspy3"
                      "mitmproxy"
                      "mitmdump"
                      "mitmweb"
                      "vpnhood"
                      "warp"
                      "warp-svc"]

STRING_SEPARATOR = "\x00"      # process names can't have a null byte in them so will use as separator
PROCESS_SUFFIX = ".exe"        # all process names end in .exe


def get_all_process_names():
    return [process.name().lower() for process in process_iter()]


def construct_process_trie():
    """
    In order to efficiently compare several different strings against a large text, I've decided to use a Trie data
    structure. Naive comparisons of two texts against each other are O(m*n^2). Using a Trie structure, we can get this
    down to O(n+m), which scales *much* better when a lot of processes are running.

    :return: a pygtrie.StringTrie containing all process names currently running on the computer.
    """

    trie = StringTrie(separator=STRING_SEPARATOR)
    for process_name in get_all_process_names():
        trie[process_name] = True   # The value stored could be the Process ID instead of True but I don't need it.
    return trie


def get_conflicts(trie, possible_conflicts=None):
    if possible_conflicts is None:
        possible_conflicts = POSSIBLE_CONFLICTS

    conflicts = []
    for entry in possible_conflicts:
        if trie.has_node(entry + PROCESS_SUFFIX) > 0:   # If there exists at least a node with this name from the head
            conflicts.append(possible_conflicts)

    return conflicts

