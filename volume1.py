# episode 1 imports

from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# episode 3 imports

from pytube import YouTube
from pprint import pprint
import inquirer

# import tkinter as tk
# from tkinter.colorchooser import askcolor
from PIL import Image, ImageDraw, ImageTk

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

class GradientPicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Gradient Color Picker")

        self.colors = []
        self.positions = []

        self.canvas = tk.Canvas(root, width=500, height=50, bg="white")
        self.canvas.pack(pady=10)

        self.add_color_button = tk.Button(root, text="Add Color", command=self.add_color)
        self.add_color_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Gradient", command=self.save_gradient)
        self.save_button.pack(pady=5)

    def indexOfSorted(self, array, value):
        # Find the position to insert the new value
        position = 0
        while position < len(array) and array[position] < value:
            position += 1

        return position

    def add_color(self):
        color = askcolor()[1]
        if color:
            position = simpledialog.askfloat("Input", "Enter position (0 to 1):", minvalue=0, maxvalue=1)
            if position is not None:
                iOS = self.indexOfSorted(self.positions, position)
                self.positions.insert(iOS, position)
                self.colors.insert(iOS, color)
                # check
                print(self.colors, self.positions)
                ###
                self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        width = 500
        height = 50
        if not self.colors:
            return

        # Create a new image to draw the gradient
        gradient = Image.new('RGB', (width, height), color=0)
        draw = ImageDraw.Draw(gradient)

        # Draw the gradient
        for i in range(len(self.colors) - 1):
            start_pos = int(self.positions[i] * width)
            end_pos = int(self.positions[i + 1] * width)
            for x in range(start_pos, end_pos):
                ratio = (x - start_pos) / (end_pos - start_pos)
                r1, g1, b1 = self.root.winfo_rgb(self.colors[i])
                r2, g2, b2 = self.root.winfo_rgb(self.colors[i + 1])
                r = int(r1 * (1 - ratio) + r2 * ratio) // 256
                g = int(g1 * (1 - ratio) + g2 * ratio) // 256
                b = int(b1 * (1 - ratio) + b2 * ratio) // 256
                draw.line([(x, 0), (x, height)], fill=(r, g, b))

        if self.colors:
            last_pos = int(self.positions[-1] * width)
            for x in range(last_pos, width):
                r, g, b = self.root.winfo_rgb(self.colors[-1])
                r = r // 256
                g = g // 256
                b = b // 256
                draw.line([(x, 0), (x, height)], fill=(r, g, b))

        # Convert the gradient image to a format tkinter can use and display it
        gradient_tk = ImageTk.PhotoImage(gradient)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=gradient_tk)
        self.canvas.image = gradient_tk

    def save_gradient(self):
        width = 500
        height = 50
        gradient = Image.new('RGB', (width, height), color=0)
        draw = ImageDraw.Draw(gradient)

        for i in range(len(self.colors) - 1):
            start_pos = int(self.positions[i] * width)
            end_pos = int(self.positions[i + 1] * width)
            for x in range(start_pos, end_pos):
                ratio = (x - start_pos) / (end_pos - start_pos)
                r1, g1, b1 = self.root.winfo_rgb(self.colors[i])
                r2, g2, b2 = self.root.winfo_rgb(self.colors[i + 1])
                r = int(r1 * (1 - ratio) + r2 * ratio) // 256
                g = int(g1 * (1 - ratio) + g2 * ratio) // 256
                b = int(b1 * (1 - ratio) + b2 * ratio) // 256
                draw.line([(x, 0), (x, height)], fill=(r, g, b))

        if self.colors:
            last_pos = int(self.positions[-1] * width)
            for x in range(last_pos, width):
                r, g, b = self.root.winfo_rgb(self.colors[-1])
                r = r // 256
                g = g // 256
                b = b // 256
                draw.line([(x, 0), (x, height)], fill=(r, g, b))

        gradient.save("gradient.png")
        messagebox.showinfo("Info", "Gradient saved as gradient.png")

def YoutubeToFileConverter():
    questions = [
        inquirer.Text('link', message="Link of video?"),
        inquirer.List(
            "extension",
            message="File extension?",
            choices=[".mp3", ".mp4"],
        )
    ]

    answers = inquirer.prompt(questions)

    # Download the YouTube video
    video_url = answers.get('link')
    yt = YouTube(video_url)
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path='.', filename=f"video{answers.get('extension')}")


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

def episode2():
    authorize("gradientpicker!", "mysticknow")
    root = tk.Tk()
    app = GradientPicker(root)
    root.mainloop()

def episode3():
    authorize("youtube 2 file converter!", "mysticknow")
    YoutubeToFileConverter()
