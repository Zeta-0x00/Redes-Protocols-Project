import random
# Packet class is used to simulate the arrival of packets to the network layer.
class Packet:
    def __init__(self, data):
        self.data = data
        self.sequence_number = random.randint(1, 4)

# Frame class is used to simulate the arrival of frames to the physical layer.
class Frame:
    def __init__(self, packet):
        self.type = 'frame'
        self.sequence_number = random.randint(0, 100)
        self.confirmation_number = packet.sequence_number
        self.data = packet.data



