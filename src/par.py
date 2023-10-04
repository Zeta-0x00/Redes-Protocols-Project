import socket
import pickle
from frame import Frame, Packet
from typing import Literal
from threading import Thread
import signal

def handler(signum, frame)-> None:
	print('good bye')
	exit(0)
signal.signal(signal.SIGINT, handler)

class ParReceiver():
	"""
		This class is used to receive the frames.
	"""
	RECEIVER_ADDR: tuple[Literal['localhost'], Literal[8009]] = ('localhost', 8009)
	sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	sock.bind(RECEIVER_ADDR)
	def __init__(self):
		...
	def receive_data(self) -> None:
		"""
			This method is used to receive the frames.
			:return: None
		"""
		print("Receiver started")
		expected_sequence_number = 0
		while True:
			frame_packet, addr = self.sock.recvfrom(1024)
			frame = pickle.loads(frame_packet)
			if frame.data == "":
				break
			if frame.sequence_number == expected_sequence_number:
				print(f"Received: {frame.data}")
				ack = Frame(Packet(""))
				ack.type = "ack"
				ack.sequence_number = expected_sequence_number
				ack.confirmation_number = expected_sequence_number
				self.sock.sendto(pickle.dumps(ack), ('localhost', 8001))
				expected_sequence_number = (expected_sequence_number + 1) % 2
			else:
				print(f"Discarding out-of-order frame with sequence_number: {frame.sequence_number}")
    
	def stop_receiver(self) -> None:
		"""
			This method is used to stop the receiver.
			:return: None
		"""
		self.sock.close()
		print("receiver has been paused")

class ParSender():
	"""
		This class is used to send the frames.
	"""
	RECEIVER_ADDR: tuple[Literal['localhost'], Literal[8009]] = ('localhost',8009)
	SENDER_ADDR: tuple[Literal['localhost'], Literal[8001]] = ('localhost', 8001)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(SENDER_ADDR)
	def __init__(self):
		...
	def send_data(self,num_frames,data)-> None:
		"""
			This method is used to send the frames.
			:param num_frames: The number of frames to send.
			:type num_frames: int
			:param data: The data to send.
			:type data: str
			:return: None
			:rtype: None
		"""
		packet: Packet = Packet(data)
		sequence_number: int = 0
		for i in range(num_frames):
			frame: Frame = Frame(packet=packet)
			frame.sequence_number = sequence_number
			self.sock.sendto(pickle.dumps(frame), self.RECEIVER_ADDR)
			print(f"Sent frame with sequence_number={sequence_number}")
			while True:
				ack_packet, addr = self.sock.recvfrom(1025)
				ack = pickle.loads(ack_packet)
				if isinstance(ack, Frame) and ack.confirmation_number == sequence_number:
					print(f"Received ACK with sequence_number={ack.confirmation_number}")
					break
			
			sequence_number: int = (sequence_number + 1) % 2
			packet.sequence_number = sequence_number
		end_frame = Frame(packet=Packet(data=""))
		end_frame.sequence_number = sequence_number
		self.sock.sendto(pickle.dumps(end_frame), self.RECEIVER_ADDR)
	def stop_sender(self)-> None:
		"""
			This method is used to stop the sender.
			:return: None
			:rtype: None
		"""
		self.sock.close()
		print("sender has been paused")

if __name__ == '__main__':
	receiver: ParReceiver = ParReceiver()
	sender: ParSender = ParSender()
	receiver_thread: Thread = Thread(target=receiver.receive_data)
	receiver_thread.start()
	sender_thread: Thread = Thread(target=sender.send_data, args=(10,"Hello"))
	sender_thread.start()
	sender_thread.join()

	try:
		receiver.stop_receiver()
		sender.stop_sender()
	except OSError:
		pass
	receiver_thread.join()
