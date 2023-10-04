import socket
import pickle
from typing import Any, NoReturn
import threading
import time
import signal

def halnder(signum, frame) -> NoReturn:
    SWSender.stop_sender()
    SWReceiver.stop_receiver()
    print('Exiting...')
    exit(0)

signal.signal(signal.SIGINT, halnder)

class Packet:
    """
        This class is used to create the packets.
    """
    def __init__(self, sequence_number, data) -> None:
        self.sequence_number: Any = sequence_number
        self.data: Any = data

class Frame:
    """
        This class is used to create the frames.
    """
    def __init__(self, window_size) -> None:
        self.window_size: Any = window_size
        self.window: list[None] = [None] * window_size
        self.expected_sequence_number = 0
        self.recv_base = 0
    def receive_packet(self, packet) -> Packet:
        """
            This method is used to receive the packets.
            :param packet: The packet.
            :type packet: Packet
            :return: The packet.
            :rtype: Packet
        """
        if packet.sequence_number >= self.expected_sequence_number and packet.sequence_number < self.expected_sequence_number + self.window_size:
            if self.window[packet.sequence_number % self.window_size] is None:
                self.window[packet.sequence_number % self.window_size] = packet
            if packet.sequence_number == self.expected_sequence_number:
                self._deliver_packets()
        return self._ack_packet(sequence_number=packet.sequence_number)
    def _ack_packet(self, sequence_number) -> Packet:
        """
            This method is used to send the ack packet.
            :param sequence_number: The sequence number.
            :type sequence_number: int
            :return: The ack packet.
            :rtype: Packet
        """
        ack_num: Any = sequence_number + 1
        return Packet(sequence_number=ack_num, data=b'')
    def _deliver_packets(self) -> None:
        """
            This method is used to deliver the packets.
            :return: None
        """
        while (d:= self.window[self.recv_base % self.window_size]) is not None:
            packet: Any = d
            self.window[self.recv_base % self.window_size] = None
            self.recv_base += 1
            self.expected_sequence_number += 1
            self._process_data(packet=packet)
    def _process_data(self, packet) -> None:        
        print(packet.data.decode('utf-8'))

class SWReceiver():
    """
        This class is used to receive the packets.
    """
    @staticmethod
    def receive_packets(listen_ip, listen_port) -> NoReturn:
        """
            This method is used to receive the packets.
            :param listen_ip: The listen ip.
            :type listen_ip: str
            :param listen_port: The listen port.
            :type listen_port: int
            :return: None
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((listen_ip, listen_port))
        frame = Frame(window_size=4)
        while True:
            data, addr = sock.recvfrom(1024)
            packet = pickle.loads(data)
            ack_packet = frame.receive_packet(packet)
            ack_data = pickle.dumps(ack_packet)
            sock.sendto(ack_data, addr)
        sock.close()
    @staticmethod
    def stop_receiver() -> None:
        """ 
            This method is used to stop the receiver.
            :return: None
        """
        global receiver
        receiver = False
        print("receiver has been paused")

class SWSender():
    """
        This class is used to send the packets.
    """
    @staticmethod
    def send_packets(packets, dest_ip, dest_port) -> None:
        """
            This method is used to send the packets.
            :param packets: The packets.
            :type packets: list
            :param dest_ip: The destination ip.
            :type dest_ip: str
            :param dest_port: The destination port.
            :type dest_port: int
            :return: None
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1.0)
        for packet in packets:
            serialized_packet: bytes = pickle.dumps(packet)
            sock.sendto(serialized_packet, (dest_ip, dest_port))
            while True:
                try:
                    ack_data, _ = sock.recvfrom(1024)
                    ack_packet = pickle.loads(ack_data)
                    if ack_packet.sequence_number == packet.sequence_number + 1:
                        break
                except socket.timeout:
                    pass
        sock.close()
    @staticmethod
    def stop_sender() -> None:
        """
            This method is used to stop the sender.
            :return: None
        """
        global sender
        sender = False
        print("Sender has been paused")

if __name__ == '__main__':
    sender_ip = '127.0.0.1'
    sender_port = 5000
    receiver_ip = '127.0.0.1'
    receiver_port = 6000
    packets: list[Packet] = [
        Packet(sequence_number=0, data=b'Kenobi:'),
        Packet(sequence_number=1, data=b'\tHello There!'),
        Packet(sequence_number=2, data=b'Grevius:'),
        Packet(sequence_number=3, data=b'\tGeneral Kenobi!'),
        Packet(sequence_number=4, data=b'\tYou are a bold one!'),
        Packet(sequence_number=5, data=b'\tKill him!'),
        Packet(sequence_number=6, data=b'*General Kenobi destroyed droids *'),
        Packet(sequence_number=7, data=b'Grevious:'),
        Packet(sequence_number=8, data=b'\tBack away! I will deal with this Jedi slime myself!'),
        Packet(sequence_number=9, data=b'Kenobi:'),
        Packet(sequence_number=10, data=b'\tYour move!'),
        Packet(sequence_number=11, data=b'Grevious:'),
        Packet(sequence_number=12, data=b'\tYou fool! I have been trained in your Jedi arts by Count Dooku!'),
        Packet(sequence_number=13, data=b'\tAttack, Kenobi!'),
        Packet(sequence_number=14, data=b'*Start of the battle*'),
    ]
    receiver_thread = threading.Thread(target=SWReceiver.receive_packets, args=(receiver_ip, receiver_port))
    receiver_thread.start()
    time.sleep(1)
    SWSender.send_packets(packets, receiver_ip, receiver_port)
    receiver_thread.join()