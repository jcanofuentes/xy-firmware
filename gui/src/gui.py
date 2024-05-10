import threading
import tkinter as tk
from tkinter import simpledialog
import serial
import struct
from tkinter import scrolledtext

# Set up the serial connection (adjust the port name and baudrate as per your setup)
SERIAL_PORT = 'COM6'  # Change this to the correct port
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
    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting).decode('utf-8', errors='replace')
            output_text.insert(tk.END, data + '\n')
            output_text.see(tk.END)

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
