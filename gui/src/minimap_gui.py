import struct
import threading
import serial
import customtkinter as ctk

class SerialPositionController:
    """
    Handles communication with a scanning device via serial port.
    Manages the position state and serial communication.
    """
    def __init__(self, serial_port, baud_rate):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.current_x = 0
        self.current_y = 0
        self.ser = None
        self.initialize_serial()

    def initialize_serial(self):
        """
        Sets up the serial connection and starts the listening thread.
        """
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            print(f"Connected to {self.serial_port}")
            self.start_reading_thread()
        except serial.SerialException:
            print("Could not open serial port. Please check the configuration.")
            exit(1)

    def start_reading_thread(self):
        """
        Starts a thread that listens for data on the serial port.
        """
        thread = threading.Thread(target=self.read_from_serial)
        thread.daemon = True
        thread.start()

    def read_from_serial(self):
        """
        Reads and processes incoming data from the serial port.
        """
        while True:
            if self.ser.in_waiting > 0:
                command = self.ser.read(1).decode('utf-8')
                value_bytes = self.ser.read(2)
                if len(value_bytes) == 2:
                    value = struct.unpack('>h', value_bytes)[0]
                    if command == 'x':
                        self.current_x = value
                    elif command == 'y':
                        self.current_y = value
                else:
                    print("Data error: Not enough bytes read.")

    def send_command(self, command, value):
        """
        Sends a command with a value to the serial device.
        """
        command_char = command.encode()
        value_short = int(value)
        value_bytes = value_short.to_bytes(2, byteorder='big', signed=True)
        self.ser.write(command_char + value_bytes)

    def request_position_update(self):
        """
        Requests the current position from the scanning device.
        """
        self.send_command('x', 0)
        self.send_command('y', 0)

    def get_current_position(self):
        """
        Returns the current x, y coordinates.
        """
        return self.current_x, self.current_y

    def close_serial(self):
        """
        Closes the serial port connection.
        """
        print("Closing serial port")
        self.ser.close()


class MotionControlPanel(ctk.CTkFrame):
    """
    A GUI panel that provides buttons for controlling motion and sending specific commands.
    """
    def __init__(self, master, serial_manager):
        super().__init__(master, corner_radius=10)
        self.serial_manager = serial_manager

        self.label = ctk.CTkLabel(self, text="Control (motion)")
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Configuración de los botones de control
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
        """
        Sends a command to move in a specified direction.
        """
        command = direction[0]  # Get the first character of the direction
        value = direction[1:]  # Get the rest of the string as the value
        self.serial_manager.send_command(command, value)

    def go_to_origin(self):
        """
        Sends a command to move the device to its origin.
        """
        self.serial_manager.send_command('O', 0)
        print("Going to Origin")

    def center_command(self):
        """
        Activates the centering function of the device.
        """
        print("Activating Center Command")

    def set_home(self):
        """
        Sets the current position as home.
        """
        print("Setting Home")

    def go_home(self):
        """
        Moves the device to the set home position.
        """
        print("Going Home")


class MinimapFrame(ctk.CTkFrame):
    """
    Displays a simple graphical representation of the position.
    """
    def __init__(self, master):
        super().__init__(master)
        self.canvas = ctk.CTkCanvas(self, width=200, height=200)
        self.canvas.pack()
        self.draw_grid()

    def draw_grid(self):
        for i in range(0, 200, 10):
            self.canvas.create_line(i, 0, i, 200, fill='gray')
            self.canvas.create_line(0, i, 200, i, fill='gray')

    def draw_rect(self, x, y):
        self.canvas.delete("rect")
        self.canvas.create_rectangle(x-5, y-5, x+10, y+10, fill='red', tags="rect")

    def clear(self):
        self.canvas.delete('all')
        self.draw_grid()

class MinimapApp(ctk.CTk):
    """
    Main application window.
    """
    def __init__(self):
        super().__init__()
        self.serial_manager = SerialPositionController('COM7', 115200)

        self.minimap = MinimapFrame(self)
        self.minimap.pack()

        self.button = ctk.CTkButton(self, text='Draw', command=self.draw)
        self.button.pack()

        self.button_clear = ctk.CTkButton(self, text='Clear', command=self.clear)
        self.button_clear.pack()

        self.motion_control = MotionControlPanel(self, self.serial_manager)
        self.motion_control.pack()

        self.start_update_loop()

    def draw(self):
        x, y = self.serial_manager.get_current_position()
        self.minimap.draw_rect(x, y)

    def clear(self):
        self.minimap.clear()

    def update(self):
        self.serial_manager.request_position_update()
        self.draw()

    def start_update_loop(self):
        self.update()
        self.after(20, self.start_update_loop)

    def on_closing(self):
        self.serial_manager.close_serial()
        self.destroy()

# Iniciar y manejar el cierre de la aplicación
app = MinimapApp()
app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()