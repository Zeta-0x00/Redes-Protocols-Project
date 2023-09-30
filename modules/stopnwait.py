from io import BufferedWriter
import pickle
import socket
import random
import time
from events.events import *
from frame.frame import Packet, Frame
from typing import Literal
from timer.timer import Timer
from threading import Thread
import signal

def handler(signum, frame)-> None:
	print('good bye')
	exit(0)
signal.signal(signal.SIGINT, handler)

class StopNWaitReceiver():
	RECEIVER_ADDR: tuple[Literal['localhost'], Literal[8025]] = ('localhost', 8025)
	sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	sock.bind(RECEIVER_ADDR)
	def receive(self) -> None:
		print(f'StopNWait Reciever', end='', flush=True)
		while True:
			packet_connect_address, addr = self.sock.recvfrom(1024)
			data_loads = pickle.loads(packet_connect_address)
			packet: Packet = Packet(data_loads)
			from_network_layer(packet)
			frame: Frame = Frame(packet)
			rand: int = packet.sequence_number
			to_physical_layer(frame)
			match rand:
				case 4:
					print('Frame Received with seqNo: ', frame.sequence_number)
					packet_connect_address = (int(frame.sequence_number) + 1) % 2
					print('Acknowlegment ', packet_connect_address, ' sent')
					self.sock.sendto(bytes(str(object=packet_connect_address), encoding='utf-8'), ('localhost', 8000))
					print('------------------------------------------------------------------')
				case 3:
					print('Frame Received with seqNo: ', frame.sequence_number)
					packet_connect_address = 'Acknowledgement Lost'
					self.sock.sendto(bytes(str(object=packet_connect_address), encoding='utf-8'), ('localhost', 8000))
					print('------------------------------------------------------------------')
				case 1 | 2:
					print('No Frame Received')
					print('------------------------------------------------------------------')
				case _:
					break
	def stop_receiver(self) -> None:
		self.sock.close()


class StopNWaitSender():
	sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	RECEIVER_ADDR: tuple[Literal['localhost'], Literal[8025]] = ('localhost', 8025)
	SENDER_ADDR: tuple[Literal['localhost'], Literal[8000]] = ('localhost', 8000)
	sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	sock.bind(SENDER_ADDR)
	def send(self, TIMEOUT_INTERVAL, SLEEP_INTERVAL, no_of_frames, data):
		send_timer = Timer(duration=TIMEOUT_INTERVAL)
		frame_to_send: int = 0
		seqNo = 0
		file: BufferedWriter = open("b.zlib", "ab")
		file.seek(0)
		file.truncate(0)
		print(f'StopNWait Sender', end='', flush=True)
		while no_of_frames > 0:
			canSend = False
			tkinter_status: list = []
			tkinter_status.extend([seqNo, data])
			while not canSend:
				packet_ack = Packet(data=data)
				rand_no: int = random.randint(a=1, b=4)
				frame: Frame = Frame(packet=packet_ack)
				from_physical_layer(r=packet_ack)
				to_network_layer(p=packet_ack)
				to_physical_layer(s=packet_ack)
				self.sock.sendto(pickle.dumps(packet_ack), ('localhost', 8025))
				send_timer.start()
				match rand_no:
					case 1:
						print('Info : ', data)
						print('Seq NO : ', seqNo)
						print('Frame Lost')
						print('Resending the frame')
						tkinter_status.append('Frame Lost')
						send_timer.stop()
						print('------------------------------------------------------------------')
					case 2:
						print('Info : ', data)
						print('Seq NO : ', seqNo)
						print('TimeOut')
						print('Resending the Frame')
						tkinter_status.append('Timeout')
						send_timer.stop()
						print('------------------------------------------------------------------')
					case 3:
						print('Info : ', data)
						print('Seq NO : ', seqNo)
						acknowledgement, _ = self.sock.recvfrom(1024)
						acknowledgement = str(acknowledgement, 'utf-8')
						print(acknowledgement)
						send_timer.stop()
						tkinter_status.append('Acknowledgement Lost')
						print('------------------------------------------------------------------')
					case 4:
						acknowledgement, _ = self.sock.recvfrom(1024)
						acknowledgement = str(acknowledgement, 'utf-8')
						print('Info : ', data)
						print('Seq NO : ', seqNo)
						print('Acknowledgement No : ', acknowledgement, ' received')
						send_timer.stop()
						canSend = True
						seqNo = (seqNo + 1) % 2
						tkinter_status.append('Acknowledgement Received')
						print('------------------------------------------------------------------')
					case _:
						...
			pickle.dump(tkinter_status, file)
			no_of_frames -= 1
		file.close()
		time.sleep(10)

	def stop_sender(self) -> None:
		self.sock.close()


if __name__ == '__main__':
	receiver: StopNWaitReceiver = StopNWaitReceiver()
	sender: StopNWaitSender = StopNWaitSender()
	receiver_thread: Thread = Thread(target=receiver.receive)
	receiver_thread.start()
	sender_thread: Thread = Thread(target=sender.send, args=(5, 2, 10, "Hello"))
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