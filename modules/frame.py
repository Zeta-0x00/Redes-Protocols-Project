import random
class Packet:
    def __init__(self, data)-> None:
        self.data = data
        self.sequence_number = random.randint(1, 4)

class Frame:
    def __init__(self, packet)-> None:
        self.type = 'frame'
        self.sequence_number = random.randint(0, 100)
        self.confirmation_number = packet.sequence_number
        self.data = packet.data



