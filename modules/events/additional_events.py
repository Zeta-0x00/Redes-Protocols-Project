import time
import random

# Events are objects that are used to simulate the arrival of events in the simulation.
class Event:
    # The time attribute is the time at which the event will occur.
    def __init__(self, time, event_type, data=None):
        self.time = time
        self.type = event_type
        self.data = data
    # The __lt__ method is used to compare events by time.
    def __lt__(self, other):
        return self.time < other.time

# FrameArrivalEvent is an event that simulates the arrival of a frame to the link layer.
class FrameArrivalEvent(Event):
    def __init__(self, time, frame):
        super().__init__(time, "frame_arrival", frame)

# CksumErrEvent is an event that simulates the arrival of a frame with checksum error to the link layer.
class CksumErrEvent(Event):
    def __init__(self, time, frame):
        super().__init__(time, "cksum_err", frame)

# TimeoutEvent is an event that simulates the expiration of the timer.
class TimeoutEvent(Event):
    def __init__(self, time):
        super().__init__(time, "timeout")

# AckTimeoutEvent is an event that simulates the expiration of the timer for the ACK.
class AckTimeoutEvent(Event):
    def __init__(self, time):
        super().__init__(time, "ack_timeout")

# NetworkLayerReadyEvent is an event that simulates the arrival of a data packet to the network layer.
class NetworkLayerReadyEvent(Event):
    def __init__(self, time, data):
        super().__init__(time, "network_layer_ready", data)


# generar_eventos() this function generates a list of events with random times.
def generar_eventos():
    # Generar eventos aleatorios
    eventos = []
    eventos.append(FrameArrivalEvent(time.time() + 2.0, b"Frame sin errores"))
    eventos.append(CksumErrEvent(time.time() + 3.0, b"Frame con errores"))
    eventos.append(TimeoutEvent(time.time() + 4.0))
    eventos.append(AckTimeoutEvent(time.time() + 5.0))
    eventos.append(NetworkLayerReadyEvent(time.time() + 1.0, b"Dato a enviar"))

    # Ordenar eventos por tiempo
    eventos.sort()

    return eventos


eventos = generar_eventos()

# Events simulation loop (this loop is not part of the simulator)
for evento in eventos:
    # Wait until the event time
    if evento.type == "frame_arrival":
        print("Evento de llegada de frame sin errores a la capa de enlace:", evento.data)
    # Wait until the event time
    elif evento.type == "cksum_err":
        print("Evento de error de checksum en la capa física:", evento.data)
    # Wait until the event time
    elif evento.type == "timeout":
        print("Evento de timeout en el timer")
    # Wait until the event time
    elif evento.type == "ack_timeout":
        print("Evento de timeout del ACK en el timer")
    # Wait until the event time
    elif evento.type == "network_layer_ready":
        print("Evento de disponibilidad de dato en la capa de red:", evento.data)
