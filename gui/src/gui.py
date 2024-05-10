import threading
import tkinter as tk
from tkinter import simpledialog
import serial
import struct
from tkinter import scrolledtext

# Set up the serial connection (adjust the port name and baudrate as per your setup)
SERIAL_PORT = 'COM7'  # Change this to the correct port
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except serial.SerialException:
    print("Could not open serial port. Please check the configuration.")
    exit(1)

def send_command():
    command = command_entry.get().strip()
    value = value_entry.get().strip()
    
    try:
        command_char = command.encode()  # Send the command as a byte
        value_short = int(value)
        # Pack the value as a short in big endian
        value_bytes = value_short.to_bytes(2, byteorder='big', signed=True)
        ser.write(command_char + value_bytes)
        print(f"Message: {command} {value_short}")
    except ValueError:
        print("Error: The command must be a character and the value must be an integer.")


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
    thread = threading.Thread(target=read_from_serial)
    thread.daemon = True
    thread.start()
    
# Set up the Tkinter GUI
root = tk.Tk()
root.title("Serial Command Sender")

# Labels and entry fields
tk.Label(root, text="Command (char):").grid(row=0, column=0)
command_entry = tk.Entry(root)
command_entry.grid(row=0, column=1)

tk.Label(root, text="Value (short):").grid(row=1, column=0)
value_entry = tk.Entry(root)
value_entry.grid(row=1, column=1)

# Button to send command
send_button = tk.Button(root, text="Send Command", command=send_command)
send_button.grid(row=2, column=0, columnspan=2)

# Text box for Arduino output
output_text = scrolledtext.ScrolledText(root, height=10, width=50)
output_text.grid(row=3, column=0, columnspan=2)

# Start receiving data on a separate thread when the GUI starts
root.after(100, start_serial_thread)

root.mainloop()

# Close the serial connection when closing the GUI
ser.close()
