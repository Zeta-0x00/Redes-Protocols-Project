#This event waits for the time specified in the event.
def wait_for_event(event):
    pass

#Fetch a packet from the network layer for transmission on the channel.
def from_network_layer(p):
    pass

#Deliver information from an inbound frame to the network layer.
def to_network_layer(p):
    pass

#Go get an inbound frame from the physical layer and copy it to r.
def from_physical_layer(r):
    pass

#Pass the frame to the physical layer for transmission.
def to_physical_layer(s):
    pass

#Start the clock running and enable the timeout event.
def start_timer(k):
    pass

#Stop the clock and disable the timeout event.
def stop_timer(k):
    pass

#Start an auxiliary timer and enable the ack timeout event.
def start_ack_timer():
    pass

#Stop the auxiliary timer and disable the ack timeout event.
def stop_ack_timer():
    pass

#Allow the network layer to cause a network layer ready event.
def enable_network_layer():
    pass

#Forbid the network layer from causing a network layer ready event.
def disable_network_layer():
    pass

#Macro inc is expanded in-line: increment k circularly.
def inc(k):
    MaxSeq = 7
    if k < MaxSeq:
        k = k + 1
    else:
        k = 0