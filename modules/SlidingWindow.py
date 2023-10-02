import socket
import pickle
from typing import Any, NoReturn, Literal
import threading
import time
import signal

def halnder(signum, frame):
    SWSender.stop_sender()
    SWReceiver.stop_receiver()
    print('Exiting...')
    exit(0)

signal.signal(signal.SIGINT, halnder)

class Packet:
    def __init__(self, sequence_number, data):
        self.sequence_number: Any = sequence_number
        self.data: Any = data

class Frame:
    def __init__(self, window_size) -> None:
        self.window_size: Any = window_size
        self.window: list[None] = [None] * window_size
        self.expected_seq_num = 0
        self.recv_base = 0
    def receive_packet(self, packet) -> Packet:
        if packet.sequence_number >= self.expected_seq_num and packet.sequence_number < self.expected_seq_num + self.window_size:
            if self.window[packet.sequence_number % self.window_size] is None:
                self.window[packet.sequence_number % self.window_size] = packet
            if packet.sequence_number == self.expected_seq_num:
                self._deliver_packets()
        return self._ack_packet(sequence_number=packet.sequence_number)
    def _ack_packet(self, sequence_number) -> Packet:
        ack_num: Any = sequence_number + 1
        return Packet(sequence_number=ack_num, data=b'')
    def _deliver_packets(self) -> None:
        while self.window[self.recv_base % self.window_size] is not None:
            packet: Any = self.window[self.recv_base % self.window_size]
            self.window[self.recv_base % self.window_size] = None
            self.recv_base += 1
            self.expected_seq_num += 1
            self._process_data(packet=packet)
    def _process_data(self, packet) -> None:
        print(packet.data.decode('utf-8'))

class SWReceiver():
    @staticmethod
    def receive_packets(listen_ip, listen_port) -> NoReturn:
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
        global receiver
        receiver = False
        print("Se ha pausado el receiver")

class SWSender():
    @staticmethod
    def send_packets(packets, dest_ip, dest_port) -> None:
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
        global sender
        sender = False
        print("Se ha pausado el sender")

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