# episode 1 imports
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
####################
import time
import random
import sys

class Whiteboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Digital Whiteboard")
        self.geometry("800x600")

        self.current_color = "#000000"
        self.pen_size = 5
        self.color_palette = []
        self.current_mode = "draw"  # Modes: "draw", "line", "move", "erase"

        self.setup_ui()
        self.bind_events()

        self.current_stroke = None
        self.strokes = []

    def setup_ui(self):
        # Canvas
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Color picker button
        self.color_picker_btn = tk.Button(self, text="Pick Color", command=self.pick_color)
        self.color_picker_btn.pack(side=tk.LEFT)

        # Pen size scale
        self.pen_size_scale = tk.Scale(self, from_=1, to=20, orient=tk.HORIZONTAL, label="Pen Size")
        self.pen_size_scale.set(self.pen_size)
        self.pen_size_scale.pack(side=tk.LEFT)

        # Color palette
        self.palette_frame = tk.Frame(self)
        self.palette_frame.pack(side=tk.LEFT)

        # Clear button
        self.clear_btn = tk.Button(self, text="Clear", command=self.clear_canvas)
        self.clear_btn.pack(side=tk.LEFT)

        # Mode selection
        self.mode_var = tk.StringVar(value="draw")
        modes = [("Draw", "draw"), ("Line", "line"), ("Move", "move"), ("Erase", "erase")]
        for text, mode in modes:
            b = tk.Radiobutton(self, text=text, variable=self.mode_var, value=mode, command=self.change_mode)
            b.pack(side=tk.LEFT)

        self.update_palette()

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def pick_color(self):
        color_code = askcolor(title="Choose color")[1]
        if color_code:
            self.current_color = color_code
            if len(self.color_palette) < 15 and color_code not in self.color_palette:
                self.color_palette.append(color_code)
                self.update_palette()

    def update_palette(self):
        for widget in self.palette_frame.winfo_children():
            widget.destroy()
        for color in self.color_palette:
            btn = tk.Button(self.palette_frame, bg=color, width=2, command=lambda c=color: self.set_color(c))
            btn.pack(side=tk.LEFT)

    def set_color(self, color):
        self.current_color = color

    def change_mode(self):
        self.current_mode = self.mode_var.get()

    def on_click(self, event):
        self.pen_size = self.pen_size_scale.get()
        if self.current_mode == "draw":
            self.current_stroke = {'type': 'draw', 'color': self.current_color, 'size': self.pen_size, 'coords': [(event.x, event.y)]}
            self.strokes.append(self.current_stroke)
        elif self.current_mode == "line":
            self.current_stroke = {'type': 'line', 'color': self.current_color, 'size': self.pen_size, 'start': (event.x, event.y), 'end': (event.x, event.y)}
            self.strokes.append(self.current_stroke)
        elif self.current_mode == "move":
            self.selected_stroke = self.find_stroke(event.x, event.y)
            if self.selected_stroke:
                self.strokes.remove(self.selected_stroke)
        elif self.current_mode == "erase":
            self.selected_stroke = self.find_stroke(event.x, event.y)
            if self.selected_stroke:
                self.strokes.remove(self.selected_stroke)
                self.redraw_canvas()

    def on_drag(self, event):
        if self.current_mode == "draw":
            x, y = event.x, event.y
            self.current_stroke['coords'].append((x, y))
            self.canvas.create_line(self.current_stroke['coords'][-2], (x, y), fill=self.current_stroke['color'], width=self.current_stroke['size'])
        elif self.current_mode == "line":
            self.current_stroke['end'] = (event.x, event.y)
            self.redraw_canvas()

    def on_release(self, event):
        if self.current_mode == "move" and self.selected_stroke:
            dx = event.x - self.selected_stroke['coords'][0][0]
            dy = event.y - self.selected_stroke['coords'][0][1]
            self.selected_stroke['coords'] = [(x + dx, y + dy) for x, y in self.selected_stroke['coords']]
            self.strokes.append(self.selected_stroke)
            self.redraw_canvas()

    def find_stroke(self, x, y):
        for stroke in self.strokes:
            for coord in stroke.get('coords', []):
                if abs(coord[0] - x) <= self.pen_size and abs(coord[1] - y) <= self.pen_size:
                    return stroke
        return None

    def redraw_canvas(self):
        self.canvas.delete("all")
        for stroke in self.strokes:
            if stroke['type'] == 'draw':
                coords = stroke['coords']
                for i in range(len(coords) - 1):
                    self.canvas.create_line(coords[i], coords[i + 1], fill=stroke['color'], width=stroke['size'])
            elif stroke['type'] == 'line':
                self.canvas.create_line(stroke['start'], stroke['end'], fill=stroke['color'], width=stroke['size'])

    def clear_canvas(self):
        self.canvas.delete("all")
        self.strokes = []

def reveal(text, duration):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  # Ensure that the character is printed immediately
        time.sleep(duration/len(text))
    print()  # Move to the next line after the text is printed

def authorize(title, author):
    print("Project Title: ", end="")
    time.sleep(0.5)
    reveal(title, 2)
    time.sleep(1)
    print("by ", end="")
    time.sleep(0.5)
    reveal(author, 1.1)

def episode1():
    authorize("whiteboard :)", "mysticknow")
    root = Whiteboard()
    root.mainloop()
