import time
from typing import Any

# Events are objects that are used to simulate the arrival of events in the simulation.
class Event:
    def __init__(self, time, type, data=None) -> None:
        # The time attribute is the time at which the event will occur.
        self.time: Any = time
        self.type: Any = type
        self.data: Any | None = data

    def __lt__(self, other) -> Any:
        # The __lt__ method is used to compare events by time.        
        return self.time < other.time

    def __str__(self) -> str:
        # The __str__ method is used to print the event.
        return f"Event: time={self.time}, type={self.type}, data={self.data}"

    def __repr__(self) -> str:
        # The __repr__ method is used to print the event.
        return self.__str__()
    
class FrameArrivalEvent(Event):
    # FrameArrivalEvent is an event that simulates the arrival of a frame to the link layer.
    def __init__(self, time, frame) -> None:
        super().__init__(time=time, type="frame_arrival", data=frame)
        
class CksumErrEvent(Event):
    # CksumErrEvent is an event that simulates the arrival of a frame with checksum error to the link layer.
    def __init__(self, time, frame) -> None:
        super().__init__(time=time, type="cksum_err", data=frame)

class TimeoutEvent(Event):
    # TimeoutEvent is an event that simulates the expiration of the timer.
    def __init__(self, time) -> None:
        super().__init__(time=time, type="timeout")

class AckTimeoutEvent(Event):
    # AckTimeoutEvent is an event that simulates the expiration of the timer for the ACK.
    def __init__(self, time) -> None:
        super().__init__(time=time, type="ack_timeout")
        
class NetworkLayerReadyEvent(Event):
    # NetworkLayerReadyEvent is an event that simulates the arrival of a data packet to the network layer.
    def __init__(self, time, data) -> None:
        super().__init__(time=time, type="network_layer_ready", data=data)
        
def generar_eventos() -> list:
    # generar_eventos() this function generates a list of events with random times.
    eventos: list = []
    eventos.append(FrameArrivalEvent(time=time.time() + 2.0, frame=b"Frame sin errores"))
    eventos.append(CksumErrEvent(time=time.time() + 3.0, frame=b"Frame con errores"))
    eventos.append(TimeoutEvent(time=time.time() + 4.0))
    eventos.append(AckTimeoutEvent(time=time.time() + 5.0))
    eventos.append(NetworkLayerReadyEvent(time=time.time() + 1.0, data=b"Dato a enviar"))

    # order events by time
    eventos.sort()

    return eventos

eventos:list = generar_eventos()



