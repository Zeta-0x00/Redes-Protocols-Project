from io import BufferedWriter
import socket
import pickle
import random
import time
from typing import Literal, NoReturn
import threading
import signal

def handler(signum, frame) -> NoReturn:
	print("Go-Back-N Protocol execution finished.")
	exit(0)

signal.signal(signal.SIGINT, handler)


class GoBackNReceiver():
	"""
		This class is used to receive the frames.
	"""
	RECEIVER_ADDR: tuple[Literal['localhost'], Literal[8025]] = ('localhost', 8025)
	SENDER_ADDR: tuple[Literal['localhost'], Literal[8000]] = ('localhost', 8000)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(RECEIVER_ADDR)
	def __init__(self) -> None:
		...
	def receiver(self)  -> NoReturn:
		"""
			This method is used to receive the frames.
			:return: None
		"""
		print(f'GoBackN Receiver', end = '', flush = True)
		while True:
			
			packet_address,addr = self.sock.recvfrom(1024)
			packet_address = pickle.loads(packet_address)
			packet: list = []
			m = int(packet_address[0])
			frame_send_at_instance = int(packet_address[1])
			arr1 = packet_address[2]
			rw = int(packet_address[3])
			f = int(packet_address[4])
			f1 = int(packet_address[5])
			if f != 5 :
				
				for i in range(frame_send_at_instance):
					if rw == int(arr1[i]) :
						
						print("Frame ",arr1[i]," is received correctly.")
						print("===============================//=================================")
						rw = (rw+1)%m
					else:
						
						print("Duplicate Frame ",arr1[i]," is discarded")
				a1: int = random.randint(0,14)
				packet.extend([rw,a1])
				self.sock.sendto(pickle.dumps(packet),addr)
			else :
				
				for i in range(f1) :
					if rw == int(arr1[i]):
						
						print("Frame ",arr1[i]," is received correctly.")
						rw: int = (rw + 1)%m
						print("===============================//=================================")
					else :
						
						print("Duplicate Frame ",arr1[i]," is discarded.")
						print("===============================//=================================")
				packet.extend([rw,f1])
				self.sock.sendto(pickle.dumps(packet),addr)
	def stop_receiver(self)  -> None:
		"""
			This method is used to stop the receiver.
		"""
		print("Se ha pausado el receiver")
		self.sock.close()

class GoBackNSender():
	"""
		This class is used to send the frames.
	"""
	RECEIVER_ADDR: tuple[Literal['localhost'], Literal[8025]] = ('localhost', 8025)
	SENDER_ADDR: tuple[Literal['localhost'], Literal[8000]] = ('localhost', 8000)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(SENDER_ADDR)
	def sender(self) -> None:
		"""
			This method is used to send the frames.
			:return: None
		"""
		total_frames = 16
		window_size = 3
		total_number_of_frames: int = pow(2, window_size)
		frame_number = 0
		frame_send_at_instance: int = total_number_of_frames // 2
		send_window = 0
		receive_window = 0
		array_to_store_the_frames_to_be_sent: list = []
		array_to_store: list = []
		size_of_the_array: int = 0
		for i in range(total_frames):
			array_to_store.append(frame_number)
			frame_number = (frame_number + 1) % total_number_of_frames
		file: BufferedWriter = open("l.zlib","ab")
		file.seek(0)
		file.truncate(0)
		
		ch = 'y'
		print(f'GoBackN Sender', end = '', flush = True)
		self.senderLoop(array_to_store, ch, file, frame_send_at_instance, receive_window, send_window, size_of_the_array,
				total_frames, total_number_of_frames)
		file.close()
		time.sleep(2)
	def senderLoop(self, array_to_store, ch, file, frame_send_at_instance, receive_window, send_window, size_of_the_array,
				total_frames, total_number_of_frames) -> None:
		"""
			This method is used to send the frames.
			:return: None
		"""
		while ch == 'y' and size_of_the_array < total_frames:
			array_to_store_the_frames_to_be_sent: list = []
			packet: list = []
			j: int = 0
			if total_frames - size_of_the_array < 4:
				frame_send_at_instance = total_frames - size_of_the_array
			for i in range(send_window, (send_window + frame_send_at_instance)):
				array_to_store_the_frames_to_be_sent.append(array_to_store[i])
				j += 1
			for i in range(j):
				
				print("Frame  ", array_to_store_the_frames_to_be_sent[i], " is sent")
			print("===============================//=================================")
			random_initial: int = random.randint(a=0, b=9)
			random_frame_instance: int = random.randint(0, frame_send_at_instance - 1)
			packet.extend(
				[total_number_of_frames, frame_send_at_instance, array_to_store_the_frames_to_be_sent, receive_window,
				random_initial, random_frame_instance])
			self.sock.sendto(pickle.dumps(packet), ('localhost', 8025))
			if random_initial != 5:
				ack, _ = self.sock.recvfrom(1024)
				ack = pickle.loads(ack)
				receive_window = int(ack[0])
				a1 = int(ack[1])
				if a1 >= 0 and a1 <= 3:
					for k in range(len(array_to_store)):
						if array_to_store_the_frames_to_be_sent[k] != array_to_store_the_frames_to_be_sent[a1]:
							print("Acknowledgement of Frame", array_to_store_the_frames_to_be_sent[k], " is recieved")
							print("===============================//=================================")
						else:
							break
					print("Acknowledgement of Frame ", array_to_store_the_frames_to_be_sent[a1], " is lost")
					print("===============================//=================================")
					temp = (send_window + frame_send_at_instance) % total_number_of_frames
					comp: int = 0
					if (temp == 0):
						comp = 7
					if int(array_to_store_the_frames_to_be_sent[a1]) == comp or int(
							array_to_store_the_frames_to_be_sent[a1]) == temp - 1:
						send_window = (send_window + 3) % total_number_of_frames
						size_of_the_array += 3
					else:
						send_window = (send_window + frame_send_at_instance) % total_number_of_frames
						size_of_the_array += 4
				else:
					send_window = (send_window + frame_send_at_instance) % total_number_of_frames
					print("All Four Frames are Acknowledged")
					print("========================================//======================================")
						   
					size_of_the_array += 4
			else:				
				ack, _ = self.sock.recvfrom(1024)
				ack = pickle.loads(ack)
				receive_window = int(ack[0])
				random_frame_instance = int(ack[1])
				ld: int = random.randint(a=0, b=1)
				if ld == 0:
					print("Frame ", array_to_store_the_frames_to_be_sent[random_frame_instance], " is damaged.")
					print("===============================//=================================")
				else:
					print("Frame ", array_to_store_the_frames_to_be_sent[random_frame_instance], " is lost")
					print("===============================//=================================")
				for i in range(random_frame_instance + 1, frame_send_at_instance):
					print("Frame ", array_to_store_the_frames_to_be_sent[i], " is discarded")
				print("//===============//TIMEOUT//===============//")
				send_window = array_to_store_the_frames_to_be_sent[random_frame_instance]
			pickle.dump(packet, file)
			ch: str = input('Send Again(y/n) : ')
			if ch != 'y':				
				break
	def stop_sender(self) -> None:
		"""
			This method is used to stop the sender.
			:return: None
		"""
		self.sock.close()
		print("Se ha pausado el sender")

if __name__ == '__main__':
	sender = GoBackNSender()
	receiver = GoBackNReceiver()
	t1 = threading.Thread(target = sender.sender)
	t2 = threading.Thread(target = receiver.receiver)
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	print("Go-Back-N Protocol execution finished.")