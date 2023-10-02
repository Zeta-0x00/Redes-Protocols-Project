import flet as ft
from threading import Thread
from par import *


def main(page):

    page.title = "Simulador de Protocolos"

    def PAR_protocol(dict):
        receiver: ParReceiver = ParReceiver()
        sender: ParSender = ParSender()
        receiver_thread: Thread = Thread(target=receiver.receive_data)
        receiver_thread.start()
        sender_thread: Thread = Thread(target=sender.send_data, args=(dict[N_frames], dict[Datos]))
        sender_thread.start()
        sender_thread.join()

    # Falta crear clases Sender y Receiver de cada protocolo
    # Crear los hilos
    # Crear botón de pausar y matar los hilos y sockets 

    def protocol_call(args: dict):
        
        match protocol_selector.value:
            case "PAR":
                PAR_protocol(dict)
            case "Utopia":
                print("u call Zootopia XD")
            case "Sliding Window 1 bit":
                print("Hello there!")
            case "Selective Repeat":
                print("Selective Repeat")
            case "Go Back N":
                print("Go Back N")
            case "Stop N Wait":
                print(f"{args.get('Timeout', None)}")
            case _:
                print("Nopi")

    def protocol_selection(e):
        protocolo.value = (f"El protocolo es: {protocol_selector.value}")
        page.update()
        page.add(N_frames)
        page.add(Datos)
        match protocol_selector.value:
            case "Stop N Wait":
                page.clean()
                page.clean()
                page.add(
                    protocol_selector,
                    protocolo,     
                )

                protocolo.value = (f"El protocolo es: {protocol_selector.value}")
                page.add(N_frames)
                page.add(Datos)

                page.add((Timeout := ft.TextField(label = "Intérvalo Timeout")))
                page.add(Sleep)
                page.add(ft.ElevatedButton("Enviar", on_click=lambda e: protocol_call({'event':e, "Timeout":Timeout.value})))
                page.update()
            
            case _:
                page.clean()
                page.add(
                    protocol_selector,
                    protocolo,     
                )

                protocolo.value = (f"El protocolo es: {protocol_selector.value}")
                page.add(N_frames)
                page.add(Datos)
                page.add(ft.ElevatedButton("Enviar", on_click=lambda e: protocol_call({'event':e, "N_frames": N_frames.value, "Datos": Datos.value})))
        
    protocolo = ft.Text()
    N_frames = ft.TextField(label = "Coloque el número de frames")
    Datos = ft.TextField(label="Datos a transferir")
    Sleep = ft.TextField(label= "Intervalo de pausa") 
    #Timeout = ft.TextField(label= "Intervalo Timeout") 

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
