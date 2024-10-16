import tkinter as tk
from scapy.all import sniff, AsyncSniffer
import threading

class IDSApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Detección de Intrusos")
        
        # Ajustar el tamaño de la ventana
        self.master.geometry("600x400")  # Ancho x Alto

        self.start_button = tk.Button(master, text="Iniciar Detección", command=self.start_detection)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(master, text="Detener Detección", command=self.stop_detection, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        # Crear un marco para contener el Text y el Scrollbar
        self.frame = tk.Frame(master)
        self.frame.pack(pady=5)

        # Crear el widget de texto
        self.output_text = tk.Text(self.frame, height=35, width=100)  # Aumentar el ancho
        self.output_text.pack(side=tk.LEFT)

        # Crear la barra de desplazamiento
        self.scrollbar = tk.Scrollbar(self.frame, command=self.output_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar el Text para usar la barra de desplazamiento
        self.output_text.config(yscrollcommand=self.scrollbar.set)

        self.sniffer = None  # Variable para almacenar el sniffer

    def packet_callback(self, packet):
        self.output_text.insert(tk.END, str(packet) + "\n")
        self.output_text.see(tk.END)

    def start_detection(self):
        self.start_button.config(state=tk.DISABLED)  # Deshabilitar botón de inicio
        self.stop_button.config(state=tk.NORMAL)      # Habilitar botón de detener
        self.sniffer = AsyncSniffer(prn=self.packet_callback, store=0)  # Usar AsyncSniffer
        self.sniffer.start()  # Iniciar la captura en un hilo separado

    def stop_detection(self):
        if self.sniffer:
            self.sniffer.stop()  # Detener la captura
            self.sniffer.join()   # Asegurarse de que el hilo termine
        self.start_button.config(state=tk.NORMAL)  # Habilitar botón de inicio
        self.stop_button.config(state=tk.DISABLED)  # Deshabilitar botón de detener

if __name__ == "__main__":
    root = tk.Tk()
    app = IDSApp(root)
    root.mainloop()
