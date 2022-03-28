import queue
from base64 import decodebytes
from pydivert import Packet
from datetime import datetime
from enum import Enum, auto
from multiprocessing import Process


class BlockReason(Enum):
    ALLOWED = 0
    DROP_INC_80 = auto()
    DROP_CLIENT_POST = auto()
    DROP_LENGTH = auto()


MAX_IP_LENGTH = len("255.255.255.255:12345")    # 21


def str_pad_right(string, pad_to=MAX_IP_LENGTH, padding=" "):
    pad_amount = pad_to - len(string)
    if pad_amount < 0: raise ValueError("Couldn't pad string: length of string is greater than pad_to")
    return string + (padding * pad_amount)


class Logger:

    def __init__(self, proxy_queue, where_to_save="logger.log"):
        self.where_to_save = where_to_save
        self.queue = proxy_queue
        self.proc = Process(target=self.process_loop, args=())
        self.proc.daemon = True
        self.stop_processing = False

    def add_packet(self, packet_as_base64, packet_interface, packet_direction,
                   packet_allowed, block_reason=BlockReason.ALLOWED):
        # This will be called from the filtering thread, pushing the encoded packet into the queue.
        # The processing / logging is run in a different thread, which pops the packet and writes info to the file.
        self.queue.put((packet_as_base64, packet_interface, packet_direction, packet_allowed, block_reason))

    def process_item(self, blocking=True, timeout=3):
        # If there is a packet then get it, else wait for one. Packets are encoded as base64 because the Packet class
        # uses memoryview types which are great but you can't pickle them (i.e. can't pipe them to different processes).
        try:
            item = self.queue.get(blocking, timeout)
            #print(item)
            try:
                (packet_base64, interface, direction, allowed, reason) = item
                packet = Packet(decodebytes(packet_base64), interface, direction)  # Decode the and recreate the packet.
                self.add_message(Logger.construct_packet_debug_info(packet, allowed, reason))
            except (ValueError, TypeError):
                self.add_message(str(item))  # ghetto fix for also allowing strings
        except queue.Empty:
            pass

    def start(self):
        self.proc.start()

    def stop(self):
        self.stop_processing = True     # We need this setting so that process_loop() will eventually return.
        self.proc.terminate()

    # This needs to be run in its' own thread, will infinitely process items as they're pushed into the queue.
    # Note that we wait for packets, but timeout every 3 seconds so that we can keep checking the while loop condition.
    def process_loop(self):
        while not self.stop_processing:
            self.process_item()

    @staticmethod
    def construct_packet_debug_info(packet, allowed, reason):
        protocol = "UDP" if packet.udp is not None else "TCP"
        decision = "ALLOWED" if allowed else "DROPPED"
        rule = "" if reason == BlockReason.ALLOWED else reason.name
        length = str(len(packet.payload))
        source = packet.src_addr + ":" + str(packet.src_port)
        destination = packet.dst_addr + ":" + str(packet.dst_port)
        #print("Parts:", protocol, destination, rule, length, source, destination)
        message = protocol+" PACKET "+decision+" FROM "+str_pad_right(source)+" -> "+\
            str_pad_right(destination)+" Len:"+str_pad_right(length, 8)+" Reason:"+rule
        return message

    def add_message(self, msg):
        Logger.static_add_message(msg, self.where_to_save)

    @staticmethod
    def static_add_message(msg, where_to_save="logger.log"):
        timestamp = "["+Logger.get_timestamp()+"] "
        message = msg.replace('\n', '\n'+timestamp)   # If this message is multiline, add the timestamp to each line.
        handle = Logger.get_handle(where_to_save)
        handle.write(timestamp + message + '\n')
        handle.close()

    @staticmethod
    def get_handle(file):
        return open(file, "a")

    @staticmethod
    def get_timestamp():
        return str(datetime.now().isoformat(sep=" "))