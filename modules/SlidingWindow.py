import socket
import pickle
from typing import Any, NoReturn, Literal
import threading
import time
import signal

def halnder(signum, frame):
    SWSender.stop_sw_sender()
    SWReceiver.stop_sw_receiver()
    print('Exiting...')
    exit(0)

signal.signal(signal.SIGINT, halnder)

class Packet:
    def __init__(self, seq_num, data):
        self.seq_num: Any = seq_num
        self.data: Any = data

class Frame:
    def __init__(self, window_size) -> None:
        self.window_size: Any = window_size
        self.window: list[None] = [None] * window_size
        self.expected_seq_num = 0
        self.recv_base = 0
    def receive_packet(self, packet) -> Packet:
        if packet.seq_num >= self.expected_seq_num and packet.seq_num < self.expected_seq_num + self.window_size:
            if self.window[packet.seq_num % self.window_size] is None:
                self.window[packet.seq_num % self.window_size] = packet
            if packet.seq_num == self.expected_seq_num:
                self._deliver_packets()
        return self._ack_packet(seq_num=packet.seq_num)
    def _ack_packet(self, seq_num) -> Packet:
        ack_num: Any = seq_num + 1
        return Packet(seq_num=ack_num, data=b'')
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
    def stop_sw_receiver() -> None:
        global receiver
        receiver = False

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
                    if ack_packet.seq_num == packet.seq_num + 1:
                        break
                except socket.timeout:
                    pass
        sock.close()
    @staticmethod
    def stop_sw_sender() -> None:
        global sender
        sender = False

if __name__ == '__main__':
    sender_ip = '127.0.0.1'
    sender_port = 5000
    receiver_ip = '127.0.0.1'
    receiver_port = 6000
    packets: list[Packet] = [
        Packet(seq_num=0, data=b'Kenobi:'),
        Packet(seq_num=1, data=b'\tHello There!'),
        Packet(seq_num=2, data=b'Grevius:'),
        Packet(seq_num=3, data=b'\tGeneral Kenobi!'),
        Packet(seq_num=4, data=b'\tYou are a bold one!'),
        Packet(seq_num=5, data=b'\tKill him!'),
        Packet(seq_num=6, data=b'*General Kenobi destroyed droids *'),
        Packet(seq_num=7, data=b'Grevious:'),
        Packet(seq_num=8, data=b'\tBack away! I will deal with this Jedi slime myself!'),
        Packet(seq_num=9, data=b'Kenobi:'),
        Packet(seq_num=10, data=b'\tYour move!'),
        Packet(seq_num=11, data=b'Grevious:'),
        Packet(seq_num=12, data=b'\tYou fool! I have been trained in your Jedi arts by Count Dooku!'),
        Packet(seq_num=13, data=b'\tAttack, Kenobi!'),
        Packet(seq_num=14, data=b'*Start of the battle*'),
    ]
    receiver_thread = threading.Thread(target=SWReceiver.receive_packets, args=(receiver_ip, receiver_port))
    receiver_thread.start()
    time.sleep(1)
    SWSender.send_packets(packets, receiver_ip, receiver_port)
    receiver_thread.join()