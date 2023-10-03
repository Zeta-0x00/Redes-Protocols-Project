import flet as ft
from threading import Thread
import socket
from par import *
from GoBackN import *
from utopia import *
from stopnwait import *
from SelectiveRepeate import *
from SlidingWindow import *

def main(page):

    page.title = "Simulador de Protocolos"

    def anadir_boton_stop(receiver, receiver_thread: Thread, sender):
        page.add(ft.ElevatedButton("Pausar Simulación", on_click=lambda e: stop_protocol(receiver, receiver_thread, sender)))
        page.update()

    def stop_protocol(receiver, receiver_thread: Thread, sender):
        page.add(ft.Text("Se está pausado la simulación"))
        page.update()
        receiver.stop_receiver()
        sender.stop_sender()
        receiver_thread.join()

    def PAR_protocol(data : dict):
        receiver: ParReceiver = ParReceiver()
        sender: ParSender = ParSender()
        receiver_thread: Thread = Thread(target=receiver.receive_data)
        receiver_thread.start()
        sender_thread: Thread = Thread(target=sender.send_data, args=(int(data.get('N_frames', 1)), data.get('Datos', "Hello there!")))
        sender_thread.start()

        anadir_boton_stop(receiver, receiver_thread, sender)
        sender_thread.join()

    
    def Utopia_protocol(data: dict):
        sender:UtopiaSender = UtopiaSender()
        receiver:ParReceiver = UtopiaReceiver()
        receiver_thread: Thread = Thread(target=receiver.receiver)
        receiver_thread.start()
        sender_thread = Thread(target=sender.send, args=(float(data.get('Timeout',0.5)), float(data.get('Sleep',0.05)), int(data.get('N_frames', 1)), data.get('Datos', 'Hello World')))
        sender_thread.start()

        anadir_boton_stop(receiver, receiver_thread, sender)
        sender_thread.join()

    def StopNwait_protocol(data: dict):
        receiver: StopNWaitReceiver = StopNWaitReceiver()
        sender: StopNWaitSender = StopNWaitSender()
        receiver_thread: Thread = Thread(target=receiver.receive)
        receiver_thread.start()
        sender_thread: Thread = Thread(target=sender.send, args=(float(data.get('Timeout',5)), float(data.get('Sleep', 2)), int(data.get('N_frames', 1)), data.get('Datos', 'Hello World')))
        sender_thread.start()
        
        anadir_boton_stop(receiver, receiver_thread, sender)
        sender_thread.join()
    
    def SlidingWindow_protocol(data: dict):
        receiver: SWReceiver = SWReceiver()
        sender: SWSender = SWSender()
        packets: list[Packet] = [
        Packet(sequence_number=0, data=b'Kenobi:'),
        Packet(sequence_number=1, data=b'\tHello There!'),
        Packet(sequence_number=2, data=b'Grevius:'),
        Packet(sequence_number=3, data=b'\tGeneral Kenobi!'),
        Packet(sequence_number=4, data=b'\tYou are a bold one!'),
        Packet(sequence_number=5, data=b'\tKill him!'),
        Packet(sequence_number=6, data=b'*General Kenobi destroyed droids *'),
        Packet(sequence_number=7, data=b'Grevious:'),
        Packet(sequence_number=8, data=b'\tBack away! I will deal with this Jedi slime myself!'),
        Packet(sequence_number=9, data=b'Kenobi:'),
        Packet(sequence_number=10, data=b'\tYour move!'),
        Packet(sequence_number=11, data=b'Grevious:'),
        Packet(sequence_number=12, data=b'\tYou fool! I have been trained in your Jedi arts by Count Dooku!'),
        Packet(sequence_number=13, data=b'\tAttack, Kenobi!'),
        Packet(sequence_number=14, data=b'*Start of the battle*'),
        ]
        receiver_ip: str = data.get('receiver_ip','127.0.0.1')
        receiver_port: int = int(data.get('receiver_port', 6000))
        receiver_thread : Thread = Thread(target=receiver.receive_packets, args=(receiver_ip, receiver_port ))
        receiver_thread.start()
        time.sleep(1)
        SWSender.send_packets(packets, receiver_ip, receiver_port)
        
        anadir_boton_stop(receiver, receiver_thread, sender)
    
    def SelectiveRepeat_protocol(data: dict):
        receiver: SRReceiver = SRReceiver()
        sender: SRSender = SRSender()
        thread_receiver = threading.Thread(target=receiver.receiver)
        thread_sender = threading.Thread(target=sender.sender, args=(int(data.get('N_frames', 1)), data.get('Datos', "Hello there!")))
        thread_receiver.start()
        thread_sender.start()
        
        anadir_boton_stop(receiver, thread_receiver, sender)
        thread_sender.join()

    def GoBackN_protocol(data: dict):
        sender = GoBackNSender()
        receiver = GoBackNReceiver()
        thread_sender = threading.Thread(target = sender.sender)
        thread_receiver = threading.Thread(target = receiver.receiver)
        thread_sender.start()
        thread_receiver.start()
        
        anadir_boton_stop(receiver, thread_receiver, sender)
        thread_sender.join()
	

    def protocol_call(args: dict):
        
        match protocol_selector.value:
            case "PAR":
                PAR_protocol(args)
            case "Utopia":
                Utopia_protocol(args)
            case "Sliding Window 1 bit":
                SlidingWindow_protocol(args)
            case "Selective Repeat":
                SelectiveRepeat_protocol(args)
            case "Go Back N":
                GoBackN_protocol(args)
            case "Stop N Wait":
                StopNwait_protocol(args)
            case _:
                print("Error al seleccionar el protocolo")

    def protocol_selection(e):
        protocolo.value = (f"El protocolo es: {protocol_selector.value}")
        page.update()
        match protocol_selector.value:
            case "Stop N Wait" | "Utopia":
                page.clean()
                page.clean()
                page.add(
                    protocol_selector,
                    protocolo,     
                )

                protocolo.value = (f"El protocolo es: {protocol_selector.value}")
                page.add((N_frames := ft.TextField(label = "Coloque el número de frames")))
                page.add((Datos := ft.TextField(label="Datos a transferir")))

                page.add((Timeout := ft.TextField(label = "Intérvalo Timeout")))
                page.add((Sleep := ft.TextField(label= "Intervalo de pausa")))
                """
                lambda = ()=> { }
                (event e) => {
                    protocol_call({
                    "event": e,
                    "Timeout": Timeout.value : str
                    })
                }
                """
                page.add(ft.ElevatedButton("Enviar", on_click=lambda e: protocol_call({'N_frames': N_frames.value, 'Datos': Datos.value, 'Timeout':Timeout.value, 'Sleep': Sleep.value})))
                page.update()
            
            case "Sliding Window 1 bit":
                page.clean()
                page.add(
                    protocol_selector,
                    protocolo,     
                )
                protocolo.value = (f"El protocolo es: {protocol_selector.value}")
                page.add((receiver_ip := ft.TextField(label = "Dirección IP del que recibe")))
                page.add((receiver_port := ft.TextField(label = "Puerto del que recibe")))
                page.add(ft.ElevatedButton("Enviar", on_click=lambda e: protocol_call({'receiver_ip': receiver_ip.value, 'receiver_port': receiver_port.value})))
            
            case _:
                page.clean()
                page.add(
                    protocol_selector,
                    protocolo,     
                )

                protocolo.value = (f"El protocolo es: {protocol_selector.value}")
                page.add((N_frames := ft.TextField(label = "Coloque el número de frames")))
                page.add((Datos := ft.TextField(label="Datos a transferir")))
                page.add(ft.ElevatedButton("Enviar", on_click=lambda e: protocol_call({'N_frames': N_frames.value, 'Datos': Datos.value})))
      
        
    protocolo = ft.Text()

    protocol_selector = ft.Dropdown(
        width=200,
        label="Protocolo",
        on_change= protocol_selection,
        options=[
            ft.dropdown.Option("PAR"),
            ft.dropdown.Option("Stop N Wait"),
            ft.dropdown.Option("Utopia"),
            ft.dropdown.Option("Go Back N"),
            ft.dropdown.Option("Selective Repeat"),
            ft.dropdown.Option("Sliding Window 1 bit"),
        ],)

    

    #first_name = ft.TextField(label="First name", autofocus=True)
    #last_name = ft.TextField(label="Last name")
    #age = ft.TextField(label="Age")
    #greetings = ft.Column()

    """def btn_click(e):
        greetings.controls.append(ft.Text(f"Hello {first_name.value} {last_name.value}! tienes {age.value} años"))
        first_name.value = ""
        last_name.value = ""
        age.value = ""
        page.update()
        first_name.focus()"""
    

    page.add(
        protocol_selector,
        protocolo,     
    )

ft.app(target=main)
