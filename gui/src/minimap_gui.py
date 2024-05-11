# Create a class for the minimap GUI

# it is a frame with a canvas
# It will:
# - draw a grid at the beginning
# - funtion to draw a rectangle of 10x10 pixels using a x,y coordinate
# - function to clear the canvas

import struct
import threading
from customtkinter import *
import customtkinter as ctk
import serial


class MotionControlFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, corner_radius=10)

        # Label for the frame
        self.label = ctk.CTkLabel(self, text="Control (motion)")
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Buttons for motion control, arranged as a cross
        self.btn_y_minus = ctk.CTkButton(self, text="Move Y", command=lambda: self.move("Y-100"))
        self.btn_y_minus.grid(row=1, column=1, pady=2, sticky="nsew")

        self.btn_x_minus = ctk.CTkButton(self, text="Move X", command=lambda: self.move("X-100"))
        self.btn_x_minus.grid(row=2, column=0, padx=2, sticky="nsew")

        self.btn_center = ctk.CTkButton(self, text="Center", command=self.center_command)
        self.btn_center.grid(row=2, column=1, padx=1, pady=1, sticky="nsew")

        self.btn_x_plus = ctk.CTkButton(self, text="Move X", command=lambda: self.move("X+100"))
        self.btn_x_plus.grid(row=2, column=2, padx=2, sticky="nsew")

        self.btn_y_plus = ctk.CTkButton(self, text="Move Y", command=lambda: self.move("Y+100"))
        self.btn_y_plus.grid(row=3, column=1, pady=2, sticky="nsew")

        # Additional control buttons
        self.btn_origin = ctk.CTkButton(self, text="Go to Origin", command=self.go_to_origin)
        self.btn_origin.grid(row=4, column=0, pady=2, sticky="nsew", columnspan=3)

        self.btn_set_home = ctk.CTkButton(self, text="Set Home", command=self.set_home)
        self.btn_set_home.grid(row=5, column=0, pady=2, sticky="nsew", columnspan=3)

        self.btn_go_home = ctk.CTkButton(self, text="Go Home", command=self.go_home)
        self.btn_go_home.grid(row=6, column=0, pady=2, sticky="nsew", columnspan=3)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def move(self, direction):
        command = direction[0]  # Get the first character of the direction
        value = direction[1:]  # Get the rest of the string as the value
        send_command(command, value)

    def go_to_origin(self):
        send_command('O', 0)
        print("Going to Origin")  # Placeholder for actual command

    def center_command(self):
        print("Activating Center Command")  # Placeholder for central button action

    def set_home(self):
        print("Setting Home")  # Placeholder for actual command

    def go_home(self):
        print("Going Home")  # Placeholder for actual command


class MinimapFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.canvas = ctk.CTkCanvas(self, width=200, height=200)
        self.canvas.pack()
        self.grid = self.draw_grid()
        self.rect = None

    def draw_grid(self):

        for i in range(0, 200, 10):
            self.canvas.create_line(i, 0, i, 200, fill='gray')
            self.canvas.create_line(0, i, 200, i, fill='gray')

    def draw_rect(self, x, y):
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(x, y, x+10, y+10, fill='red')

    def clear(self):
        self.canvas.delete('all')
        self.draw_grid()

class MinimapApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.minimap = MinimapFrame(self)
        self.minimap.pack()

        self.button = ctk.CTkButton(self, text='Draw', command=self.draw)
        self.button.pack()

        self.button_clear = ctk.CTkButton(self, text='Clear', command=self.clear)
        self.button_clear.pack()

        self.motion_control = MotionControlFrame(self)
        self.motion_control.pack()

    def draw(self):
        self.minimap.draw_rect(50, 50)
    def clear(self):
        self.minimap.clear()

def read_from_serial():
    expected_data_size = struct.calcsize('ch')  # Calcula el tamaño de la estructura 'char' + 'short' (2 bytes + 1 byte)
    
    while True:
        if ser.in_waiting > 0:
            command = ser.read(1)  # Leer el byte del comando
            # Convert to char
            command = command.decode('utf-8')
            value_bytes = ser.read(2)  # Leer los 2 bytes del valor
            if len(value_bytes) == 2:
                # Unpack the value as a short in big endian
                value = struct.unpack('>h', value_bytes)[0]
                print(f"Command: {command}, Value: {value}")
            else:
                print("Data error: Not enough bytes read.")

def start_serial_thread():
    print("Starting serial thread")
    thread = threading.Thread(target=read_from_serial)
    thread.daemon = True
    thread.start()

    
def send_command( command, value ):
    try:
        command_char = command.encode()  # Send the command as a byte
        value_short = int(value)
        # Pack the value as a short in big endian
        value_bytes = value_short.to_bytes(2, byteorder='big', signed=True)
        ser.write(command_char + value_bytes)
        print(f"Message: {command} {value_short}")
    except ValueError:
        print("Error: The command must be a character and the value must be an integer.")


# Set up the serial connection (adjust the port name and baudrate as per your setup)
SERIAL_PORT = 'COM7'  # Change this to the correct port
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT}")
except serial.SerialException:
    print("Could not open serial port. Please check the configuration.")
    exit(1)

# Start receiving data on a separate thread when the GUI starts
start_serial_thread()

app = MinimapApp()
app.mainloop()






