from io import BufferedWriter
import pickle
import socket
import time
from events.events import *
from frame.frame import Packet, Frame
from typing import Literal
from timer.timer import Timer
from threading import Thread
import signal
import sys

def handler(signum, frame)-> None:
	print('good bye')
	sys.exit(0)
signal.signal(signal.SIGINT, handler)

class UtopiaReceiver():
	RECEIVER_ADDR: tuple[Literal['localhost'], Literal[8026]] = ('localhost', 8026)
	sock: socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	sock.bind(RECEIVER_ADDR)
	def __init__(self) -> None:
		self.running = True
	def recreive(self) -> None:
		print(f'Utopia Reciever', end='', flush=True)
		while True:
			wait_for_event(event='frame_arrival')
			pkt, addr = self.sock.recvfrom(1024)
			DATA = pickle.loads(pkt)
			packet: Packet = Packet(data=DATA.data)
			frame: Frame = Frame(packet=packet)
			from_physical_layer(r=frame)
			to_network_layer(p=packet)
			print('Frame Received with seqNo: ', frame.sequence_number)
			print('Content : ', frame.data)
			print('------------------------------------------------------------------')
	
	def stop(self) -> None:
		print('Receiver Stopped')
		try:
			self.sock.close()
			self.running = False
		except OSError as e:
			pass

class UtopiaSender():
	sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	RECEIVER_ADDR: tuple[Literal['localhost'], Literal[8026]] = ('localhost', 8026)
	SENDER_ADDR: tuple[Literal['localhost'], Literal[8030]] = ('localhost', 8030)
	sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	sock.bind(SENDER_ADDR)
	frame_to_send = 0
	tkinter_status = []
	def __init__(self) -> None:
		...
	def send(self, TIMEOUT_INTERVAL, SLEEP_INTERVAL, no_of_frames, data) -> None:
		seqNo = 0
		send_timer = Timer(duration=TIMEOUT_INTERVAL)
		file: BufferedWriter = open("b.txt", "ab")
		file.seek(0)
		file.truncate(0)
		print(f'Utopia Sender', end='', flush=True)
		while no_of_frames > 0:
			canSend = False
			tkinter_status = [seqNo, data]
			while not canSend:
				packet = Packet(data)
				frame = Frame(packet)
				from_network_layer(packet)
				self.sock.sendto(pickle.dumps(frame), self.RECEIVER_ADDR)
				canSend = True
				to_physical_layer(frame)
			pickle.dump(tkinter_status, file)
			no_of_frames -= 1
			seqNo += 1
		file.close()
		time.sleep(10)
	
	def stop(self) -> None:
		print('Sender Stopped')
		try:
			self.sock.close()
		except OSError:
			pass

if __name__ == '__main__':
	sender = UtopiaSender()
	receiver = UtopiaReceiver()
	receiver_thread = Thread(target=receiver.recreive)
	receiver_thread.start()
	sender_thread = Thread(target=sender.send, args=(0.5, 0.05, 3, 'Hello World'))
	sender_thread.start()
	sender_thread.join()
	try:
		sender.stop()
	except Exception:
		...
	try:
		receiver.stop()
	except Exception:
		...
	receiver_thread.join()
	time.sleep(5)
	sender_thread._stop()
	receiver_thread._stop()
	