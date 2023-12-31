from enum import Enum
import pickle
import random
import socket
import threading
import time
from typing import Any, NoReturn
import signal

def halnder(signum, frame) -> NoReturn:
	print('Exiting...')
	exit(0)

signal.signal(signal.SIGINT, halnder)


class Packet(Enum):
    data = 1
    ACK = 2
    CKSUM_ERR = 3

class Frame:
    packet = Packet
    sequence_number = 0
    confirmationNumber = 0
    packetInfo = ""
    def __init__(self, packet, sequence_number, confirmationNumber, packetInfo):
        self.packet = packet
        self.sequence_number = sequence_number
        self.confirmationNumber = confirmationNumber
        self.packetInfo = packetInfo


class SRReceiver():
	"""
		This class is used to receive the frames.	
	"""
	receiver_socket: socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	host: str = socket.gethostname()
	portA: int = 8004
	portB: int = 8006
	receiver_socket.bind(('', portB))
	def receiver(self, window_size=7) -> Any:
		"""
			This method is used to receive the frames.
			:param window_size: The window size.
			:type window_size: int
			:return: None
			:rtype: None
		"""
		total_size = 8192
		frame_size = 0
		frame_list: list = []
		expected_sequence_number = 0
		frame_size: float = (window_size + 1) / 2
		while True:
			try:
				frame_was_obtained, _ = self.receiver_socket.recvfrom(total_size)
				frame_was_obtained: Any = pickle.loads(frame_was_obtained)
				sequence_number: Any = frame_was_obtained.sequence_number
				print("\nProcesando: ", sequence_number)
				if expected_sequence_number == sequence_number and not frame_was_obtained.packet == Packet.CKSUM_ERR:
					print("Info: ", frame_was_obtained.packetInfo)
					self.receiver_socket.sendto(pickle.dumps(sequence_number), (self.host, self.portA))
					expected_sequence_number += 1
					if len(frame_list) > 0:
						print("Frames en el Buffer: ", [item.sequence_number for item in frame_list])
						expected_sequence_number += len(frame_list)
						frame_list.clear()
						print("Frame expected: ", expected_sequence_number)
					else:
						print("No frame here")
				elif sequence_number >= expected_sequence_number - frame_size / 2 and sequence_number <= expected_sequence_number + frame_size / 2 and len(
						frame_list) < frame_size:
					if not frame_was_obtained.packet == Packet.CKSUM_ERR:
						print("Info: ", frame_was_obtained.packetInfo)
						frame_list.append(frame_was_obtained)
						print("Frame esperado: ", expected_sequence_number)
						self.receiver_socket.sendto(pickle.dumps(sequence_number), (self.host, self.portA))
			except Exception as e:
				print("FATAL ERROR WITH THE FRAME")
	def stop_receiver(self) -> None:
		"""
			This method is used to stop the receiver.
			:return: None
			:rtype: None
		"""
		self.receiver_socket.close()
		print("receiver has been paused")

class SRSender():
	"""
		This class is used to send the frames.
	"""
	socket_sender: socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	host: str = socket.gethostname()
	portA: int = 8004
	portB: int = 8006
	def shipping_confirmation(self, size_buffer, lock, frames_without_confirmation, actual_ack_sequence_number) -> NoReturn:
		"""
			This method is used to confirm the frames.
			:param size_buffer: The size of the buffer.
			:type size_buffer: int
			:param lock: The lock.
			:type lock: threading.Lock
			:param frames_without_confirmation: The frames without confirmation.
			:type frames_without_confirmation: list
			:param actual_ack_sequence_number: The actual ack sequence number.
			:type actual_ack_sequence_number: int
			:return: None
			:rtype: None
		"""
		self.socket_sender.bind(('', self.portA))
		while True:
			try:
				ack, _ = self.socket_sender.recvfrom(size_buffer)
				lock.acquire()
				ack_number: Any = pickle.loads(ack)
				print("\nFrame Confirmed: ", ack_number)
				actual_ack_sequence_number: Any = ack_number
				frames_without_confirmation.remove(ack_number)
				lock.release()
			except Exception as e:
				print("Error: ", e)
	def next_frame(self, frames_window, counter_window) -> Any:
		"""
			This method is used to get the next frame.
			:param frames_window: The frames window.
			:type frames_window: list
			:param counter_window: The counter window.
		"""
		next_frame_to_send = frames_window[counter_window]
		counter_window += 1
		return next_frame_to_send
	def sender_window(self, packet, frame_type, frames_window, actual_sequence_number) -> None:
		"""
			This method is used to send the frames.
			:param packet: The packet.
			:type packet: Packet
			:param frame_type: The frame type.
			:type frame_type: list
			:param frames_window: The frames window.
		"""
		frame_to_send = Frame(random.choice(frame_type), actual_sequence_number, -1, packet)
		frames_window.append(frame_to_send)
		actual_sequence_number += 1
	def sender(self, window_size, packet) -> None:
		"""
			This method is used to send the frames.
			:param window_size: The window size.
			:type window_size: int
			:param packet: The packet.
			:type packet: Packet
			:return: None
		"""
		counter_window = 0
		size_buffer = 1024
		frames_without_confirmation: list = []
		frames_window: list = []
		attempts = 0
		actual_sequence_number = 0
		actual_ack_sequence_number = -1
		lock = threading.Lock()
		# network_layer_flag is used to get the network layer flag.
		network_layer_flag = True
		# frame_type is used to get the frame type.
		frame_type = [Packet.data,
					Packet.CKSUM_ERR]
		# attempts is used to get the attempts.
		attempts = (window_size + 1) / 2
		# thread is used to get the thread.
		thread = threading.Thread(target=self.shipping_confirmation,
								args=(size_buffer, lock, frames_without_confirmation, actual_ack_sequence_number))
		thread.start()
		# This loop is used to send the frames to the receiver.
		while True:
			# This if is used to send the frames to the receiver.
			if len(frames_window) < window_size and network_layer_flag:
				self.sender_window(packet, frame_type, frames_window, actual_sequence_number)
			# This else is used to send the frames to the receiver.
			else:
				# network_layer_flag is used to get the network layer flag.
				network_layer_flag = False
				# This if is used to send the frames to the receiver.
				time.sleep(1.5)
				# This if is used to send the frames to the receiver.
				lock.acquire()
				# frame_to_send is used to get the frame to send.
				frame_to_send = self.next_frame(frames_window, counter_window)
				# counter_window is used to get the counter window.
				frames_without_confirmation.append(frame_to_send.sequence_number)
				# counter_window is used to get the counter window.
				serializedFrame = pickle.dumps(frame_to_send)
				print("\nSending: ", frame_to_send.sequence_number)
				print("+++++++++++++++++")
				try:
					self.socket_sender.sendto(serializedFrame, (self.host, self.portB))
				except:
					print("The execution has ended")
					return
				timer = threading.Timer(attempts, self.retry_send,
										args=(frame_to_send, frames_without_confirmation, lock, frame_type, attempts))
				timer.start()
				lock.release()
				if counter_window == window_size:
					frames_window.clear()
					counter_window = 0
					network_layer_flag = True
	def retry_send(self, frameToSend, frames_without_confirmation, lock, frame_type, attempts) -> None:
		"""
			This method is used to retry the send.
			:param frameToSend: The frame to send.
			:type frameToSend: Frame
			:param frames_without_confirmation: The frames without confirmation.
			:type frames_without_confirmation: list
			:param lock: The lock.
		"""
		lock.acquire()
		if frameToSend.sequence_number not in frames_without_confirmation:
			lock.release()
			return
		frameToSend.packet = random.choice(seq=frame_type)
		print("\nSending Again: ", frameToSend.sequence_number)
		serialized_frame: bytes = pickle.dumps(obj=frameToSend)
		try:
			self.socket_sender.sendto(serialized_frame, (self.host, self.portB))
		except:
			print("The execution has ended")
			lock.release()
			return
		timer = threading.Timer(attempts, self.retry_send,
								args=(frameToSend, frames_without_confirmation, lock, frame_type, attempts))
		timer.start()
		lock.release()
	def stop_sender(self) -> None:
		"""
			This method is used to stop the sender.
			:return: None
			:rtype: None
		"""
		self.socket_sender.close()
		print("Sender has been paused_")

if __name__ == '__main__':
	data = "Hello There!"
	receiver: SRReceiver = SRReceiver()
	sender: SRSender = SRSender()
    # Thread to receive the packets
	thread_receiver = threading.Thread(target=receiver.receiver)
	# Thread to send the packets
	thread_sender = threading.Thread(target=sender.sender, args=(7, data))
	# Start the threads
	thread_receiver.start()
	thread_sender.start()
	# Wait for the threads
	thread_receiver.join()
	thread_sender.join()
	# Stop the threads
	receiver.stop_receiver()
	sender.stop_sender()