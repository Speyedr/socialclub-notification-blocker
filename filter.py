import pydivert                                     # handles capturing and dropping or allowing packets
from socket import gethostbyname                    # get IP address from hostname
from enum import Flag, auto                         # flags and options
from re import compile, match, search, MULTILINE    # searching text / content
from multiprocessing import Process                 # Allows multi-processing (so the filter can run "behind" the UI)
from logger import Logger, BlockReason
from base64 import encodebytes


LOG_FILE = "debug.log"


class FilterFlags(Flag):
    DROP_INC_80 = auto()  # Drop incoming packets with 80-byte payloads (DTLSv1.0 from T2 / R* IP)
    DROP_CLIENT_POST = auto()  # Drop TCP segments containing the GetMessages POST request (to prs-gta5-prod.ros...)
    DROP_LENGTH = auto()  # Drop server responses based on their Content-Length attribute


"""
DROP_INC_80 works but the server will indefinitely send you updates every 8 seconds until the filter is off,
at which point you receive all your notifications.

DROP_CLIENT_POST works and eventually the TCP protocol gives up trying to send information.
"""


class DropLengthSettings:
    RESPONSE_SIZE = 518  # 518 bytes of content excluding the nickname

    def __init__(self, min_offset=0, max_offset=64):
        self.verify_offsets(self.verify_offset(min_offset), self.verify_offset(max_offset))  # yuck

        self.min_length = min_offset + DropLengthSettings.RESPONSE_SIZE
        self.max_length = max_offset + DropLengthSettings.RESPONSE_SIZE

    def bounds(self, value):
        return self.min_length <= value <= self.max_length

    @staticmethod
    def verify_offset(val):
        if val < 0:
            raise ValueError("offsets cannot be negative")
        return val

    @staticmethod
    def verify_offsets(min_val, max_val):
        if min_val > max_val:
            raise ValueError("min_val (" + str(min_val) + ") is greater than max_val (" + str(max_val) + ")")
        return min_val, max_val

    # These setters / updaters should probably verify before updating the value, also unnecessary to have two functions
    def update_min_offset(self, offset):
        self.min_length = DropLengthSettings.RESPONSE_SIZE + self.verify_offset(offset)
        self.verify_offsets(self.min_length, self.max_length)

    def update_max_offset(self, offset):
        self.max_length = DropLengthSettings.RESPONSE_SIZE + self.verify_offset(offset)
        self.verify_offsets(self.min_length, self.max_length)


class FilterSettings:
    CLIENT_POST_ENDPOINT = "/gta5/11/gameservices/Presence.asmx/GetMessages"      # Update if R* change the endpoint
    CLIENT_POST_HOST = "prs-gta5-prod.ros.rockstargames.com"                      # Update if R* change the website
    CLIENT_POST_METHOD = "POST"                                                   # Update if R* change the method
    CLIENT_POST_PROTOCOL = "HTTP/1.1"                                             # Update if R* change the protocol
    CLIENT_LINES = [CLIENT_POST_METHOD + " " + CLIENT_POST_ENDPOINT + " " + CLIENT_POST_PROTOCOL,
                    "Host: " + CLIENT_POST_HOST]                                  # Each element is a line of the header
    CLIENT_LINE_SEP = '\r\n'                                                      # The line separator
    MATCH_HEADER = compile(bytes('^'+CLIENT_LINE_SEP.join(CLIENT_LINES), 'utf-8'))# Used to match the entire header
    SERVER_IP = gethostbyname(CLIENT_POST_HOST)                                   # The IP address of the website
    SERVER_RESPONSE_LENGTH_ATTR = "Content-Length: "        # The attribute that claims the length of content returned.
    GET_RESPONSE_LENGTH = compile(
        bytes("(?<=^"+SERVER_RESPONSE_LENGTH_ATTR+r")\d+", 'utf-8'), MULTILINE)   # Get the length of content returned.
    SERVER_DTLS_PAYLOAD_LENGTH = 93      # WinDivert Bug: Payload is 80 bytes but WinDivert isn't aware of DTLS header.

    def __init__(self, flags, drop_lengths=None, logger_queue=None):
        if (flags & FilterFlags.DROP_LENGTH) and drop_lengths is None:
            raise ValueError("Flag DROP_LENGTHS is set but no drop length was given.")

        self.flags = flags
        self.drop_lengths = drop_lengths
        self.logger = logger_queue
        Logger.static_add_message("Filter flags: " + str(flags), LOG_FILE)
        if self.logger is not None:
            Logger.static_add_message("Logger supplied to FilterSettings: " + str(self.logger), LOG_FILE)
        else:
            Logger.static_add_message("Logger not supplied to FilterSettings.", LOG_FILE)

    def should_allow(self, packet):
        if (self.flags & FilterFlags.DROP_INC_80) and packet.is_inbound and packet.udp is not None \
                and len(packet.payload) == FilterSettings.SERVER_DTLS_PAYLOAD_LENGTH:
            if self.logger is not None:
                self.logger.put((encodebytes(packet.raw), packet.interface, packet.direction,
                                       False, BlockReason.DROP_INC_80))
            return False

        if (self.flags & FilterFlags.DROP_CLIENT_POST) and packet.is_outbound \
                and packet.tcp is not None and packet.dst_addr == FilterSettings.SERVER_IP \
                and match(FilterSettings.MATCH_HEADER, packet.payload):
            if self.logger is not None:
                self.logger.put((encodebytes(packet.raw), packet.interface, packet.direction,
                                       False, BlockReason.DROP_CLIENT_POST))
            return False

        if (self.flags & FilterFlags.DROP_LENGTH) and packet.is_inbound \
                and packet.tcp is not None and packet.src_addr == FilterSettings.SERVER_IP:
            content_length = search(FilterSettings.GET_RESPONSE_LENGTH, packet.payload)
            print(content_length)
            if content_length and self.drop_lengths.bounds(int(content_length.group())):
                if self.logger is not None:
                    self.logger.put((encodebytes(packet.raw), packet.interface, packet.direction,
                                           False, BlockReason.DROP_LENGTH))
                return False

        return True


class Filter:

    RSERV_MIN_PORT = "61455"    # The minimum in portrange for R* services
    RSERV_MAX_PORT = "61458"    # The maximum in portrange for R* Services

    # The following string constructions are PyDivert filters.
    FILTER_INC_80 = "(udp.SrcPort >= "+RSERV_MIN_PORT+" and udp.SrcPort <= "+RSERV_MAX_PORT+")"
    FILTER_CLIENT_POST = "(tcp.DstPort == 80 and ip.DstAddr == "+FilterSettings.SERVER_IP+")"
    FILTER_LENGTH = "(tcp.SrcPort == 80 and ip.SrcAddr == "+FilterSettings.SERVER_IP+")"

    def __init__(self, filter_settings):
        filters = [(FilterFlags.DROP_INC_80, Filter.FILTER_INC_80),
                   (FilterFlags.DROP_CLIENT_POST, Filter.FILTER_CLIENT_POST),
                   (FilterFlags.DROP_LENGTH, Filter.FILTER_LENGTH)]

        self.filter_settings = filter_settings
        selected_filters = filters   # Start with all and remove any filters that haven't been set
        i = 0
        while i < len(selected_filters):
            if not (selected_filters[i][0] & self.filter_settings.flags):  # Is this filter selected in flags?
                selected_filters.pop(i)                                    # If it isn't, remove the filter.
            else:
                i += 1

        # Now that we've removed the unwanted filters, we only want the 2nd element in the tuple (the actual string).
        reduced_filters = []
        for tup in selected_filters:
            reduced_filters.append(tup[1])

        # Now we can use string joining to produce the final overall filter based on the flags that have been set.
        self.pydivert_filter = " or ".join(reduced_filters)
        Logger.static_add_message("Using filter: " + self.pydivert_filter, LOG_FILE)
        self.proc = Process(target=self.filter_loop, args=())
        self.proc.daemon = True     # The filter process is a child of the main process.

    def start(self):
        self.proc.start()

    def stop(self):
        self.proc.terminate()

    def filter_loop(self, print_allowed=False, print_dropped=False):
        if not pydivert.WinDivert.is_registered():
            pydivert.WinDivert.register()  # "Install" WinDivert so we can use it for filtering.

        with pydivert.WinDivert(self.pydivert_filter) as w:
            for packet in w:

                if self.filter_settings.should_allow(packet):
                    w.send(packet)  # If the packet should be allowed, inject it back into the stream. (Duh)
                    if print_allowed:
                        print(Filter.construct_packet_debug_message(packet, True))
                else:
                    if print_dropped:
                        print(Filter.construct_packet_debug_message(packet, False))

    @staticmethod
    def construct_packet_debug_message(packet, packet_allowed):
        return ("ALLOWING" if packet_allowed else "DROPPING")+" PACKET FROM "+packet.src_addr+":"+str(packet.src_port)+\
                " -> "+packet.dst_addr+":"+str(packet.dst_port)+" "+("UDP" if packet.udp is not None else "TCP")+\
                " Len:"+str(len(packet.payload))
