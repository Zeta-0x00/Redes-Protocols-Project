import time

# Events are objects that are used to simulate the arrival of events in the simulation.
class Event:
    def __init__(self, time, type, data=None):
        # The time attribute is the time at which the event will occur.
        self.time = time
        self.type = type
        self.data = data

    def __lt__(self, other):
        # The __lt__ method is used to compare events by time.        
        return self.time < other.time

    def __str__(self):
        # The __str__ method is used to print the event.
        return f"Event: time={self.time}, type={self.type}, data={self.data}"

    def __repr__(self):
        # The __repr__ method is used to print the event.
        return self.__str__()
    
class FrameArrivalEvent(Event):
    # FrameArrivalEvent is an event that simulates the arrival of a frame to the link layer.
    def __init__(self, time, frame):
        super().__init__(time, "frame_arrival", frame)
        
class CksumErrEvent(Event):
    # CksumErrEvent is an event that simulates the arrival of a frame with checksum error to the link layer.
    def __init__(self, time, frame):
        super().__init__(time, "cksum_err", frame)

class TimeoutEvent(Event):
    # TimeoutEvent is an event that simulates the expiration of the timer.
    def __init__(self, time):
        super().__init__(time, "timeout")

class AckTimeoutEvent(Event):
    # AckTimeoutEvent is an event that simulates the expiration of the timer for the ACK.
    def __init__(self, time):
        super().__init__(time, "ack_timeout")
        
class NetworkLayerReadyEvent(Event):
    # NetworkLayerReadyEvent is an event that simulates the arrival of a data packet to the network layer.
    def __init__(self, time, data):
        super().__init__(time, "network_layer_ready", data)
        
def generar_eventos():
    # generar_eventos() this function generates a list of events with random times.
    eventos = []
    eventos.append(FrameArrivalEvent(time.time() + 2.0, b"Frame sin errores"))
    eventos.append(CksumErrEvent(time.time() + 3.0, b"Frame con errores"))
    eventos.append(TimeoutEvent(time.time() + 4.0))
    eventos.append(AckTimeoutEvent(time.time() + 5.0))
    eventos.append(NetworkLayerReadyEvent(time.time() + 1.0, b"Dato a enviar"))

    # order events by time
    eventos.sort()

    return eventos

eventos = generar_eventos()



