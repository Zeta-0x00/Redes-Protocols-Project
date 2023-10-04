from io import BufferedWriter
import pickle
import socket
import time
from frame import Packet, Frame
from typing import Literal
from threading import Thread
import signal
import sys

def handler(signum, frame)-> None:
	print('good bye')
	sys.exit(0)
signal.signal(signal.SIGINT, handler)

class UtopiaReceiver():
	"""
		This class is used to receive the frames.
	"""
	RECEIVER_ADDR: tuple[Literal['localhost'], Literal[8026]] = ('localhost', 8026)
	sock: socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	sock.bind(RECEIVER_ADDR)
	def __init__(self) -> None:
		self.running = True
	def receiver(self) -> None:
		"""
			This method is used to receive the frames.
			:return: None
		"""
		print(f'Utopia Reciever', end='', flush=True)
		while True:
			received_packet, addr = self.sock.recvfrom(1024)
			Datos = pickle.loads(received_packet)
			packet: Packet = Packet(data=Datos.data)
			frame: Frame = Frame(packet=packet)
			print('Frame Received with sequence_number: ', frame.sequence_number)
			print('Content : ', frame.data)
			print('===============================//=================================')
				   
	
	def stop_receiver(self) -> None:
		"""
			This method is used to stop the receiver.
			:return: None
		"""
		print("Se ha pausado el receiver")
		try:
			self.sock.close()
			self.running = False
		except OSError as e:
			pass

class UtopiaSender():
	"""	
		This class is used to send the frames.
	"""
	sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	RECEIVER_ADDR: tuple[Literal['localhost'], Literal[8026]] = ('localhost', 8026)
	SENDER_ADDR: tuple[Literal['localhost'], Literal[8030]] = ('localhost', 8030)
	sock.bind(SENDER_ADDR)
	frame_to_send = 0
	def __init__(self) -> None:
		self.running = True
	def send(self, TIMEOUT_INTERVAL, SLEEP_INTERVAL, no_of_frames, data) -> None:
		"""
			This method is used to send the frames.
			:param TIMEOUT_INTERVAL: The timeout interval.
			:type TIMEOUT_INTERVAL: float
			:param SLEEP_INTERVAL: The sleep interval.
			:type SLEEP_INTERVAL: float
			:param no_of_frames: The number of frames to send.
			:type no_of_frames: int
			:param data: The data to send.
			:type data: str
			:return: None
		"""
		sequence_number = 0
		s:float = time.time()
		with open(file="b.zlib", mode="ab") as file:
			file.seek(0)
			file.truncate(0)
			print(f'Utopia Sender', end='', flush=True)
			while no_of_frames >= 0:
				if time.time() - s > TIMEOUT_INTERVAL:
					print(f'Utopia Sender', end='', flush=True)
					break
				canSend = False
				while not canSend:
					packet = Packet(data=data)
					frame = Frame(packet=packet)
					self.sock.sendto(pickle.dumps(frame), self.RECEIVER_ADDR)
					canSend = True
				no_of_frames -= 1
				sequence_number += 1
				time.sleep(SLEEP_INTERVAL)
	
	def stop_sender(self) -> None:
		"""
			This method is used to stop the sender.
			:return: None
		"""
		print("Se ha pausado el sender")
		try:
			self.sock.close()
		except OSError:
			pass

if __name__ == '__main__':
	sender = UtopiaSender()
	receiver = UtopiaReceiver()
	receiver_thread = Thread(target=receiver.receiver)
	receiver_thread.start()
	sender_thread = Thread(target=sender.send, args=(25, 0.5, 10, 'Hello World'))
	sender_thread.start()
	sender_thread.join()
	try:
		sender.stop_sender()
	except Exception:
		...
	try:
		receiver.stop_receiver()
	except Exception:
		...
	receiver_thread.join()
	time.sleep(5)
	sender_thread._stop()
	receiver_thread._stop()
	