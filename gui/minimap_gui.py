# Create a class for the minimap GUI

# it is a frame with a canvas
# It will:
# - draw a grid at the beginning
# - funtion to draw a rectangle of 10x10 pixels using a x,y coordinate
# - function to clear the canvas

from customtkinter import *
import customtkinter as ctk


class MotionControlFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        #Round corner
        #self.config(corner_radius=10)
        #self.pack(pady=20, padx=20, fill="both", expand=True)

        # Label for the frame
        self.label = ctk.CTkLabel(self, text="Control (motion)")
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Buttons for motion control, arranged as a cross
        self.btn_y_minus = ctk.CTkButton(self, text="Move Y", command=lambda: self.move("y-6"))
        self.btn_y_minus.grid(row=1, column=1, pady=2, sticky="nsew")

        self.btn_x_minus = ctk.CTkButton(self, text="Move X", command=lambda: self.move("x-6"))
        self.btn_x_minus.grid(row=2, column=0, padx=2, sticky="nsew")

        self.btn_center = ctk.CTkButton(self, text="Center", command=self.center_command)
        self.btn_center.grid(row=2, column=1, padx=1, pady=1, sticky="nsew")

        self.btn_x_plus = ctk.CTkButton(self, text="Move X", command=lambda: self.move("x+6"))
        self.btn_x_plus.grid(row=2, column=2, padx=2, sticky="nsew")

        self.btn_y_plus = ctk.CTkButton(self, text="Move Y", command=lambda: self.move("y+6"))
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
        print(f"Moving {direction}")  # Placeholder for actual move command

    def center_command(self):
        print("Activating Center Command")  # Placeholder for central button action

    def go_to_origin(self):
        print("Going to Origin")  # Placeholder for actual command

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

if __name__ == '__main__':

    app = MinimapApp()
    app.mainloop()


