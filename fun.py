import tkinter as tk
import random

def fun():
    def on_random_choice_button_click():
        choice = random.choice(['Yes', 'No', 'Close'])
        if choice == 'Close':
            root.destroy()
        else:
            choice_label.config(text=choice)

    def on_generate_code_button_click():
        code = ''.join(random.choices('0123456789', k=4))
        code_label.config(text=code)

    def on_guess_button_click():
        guessed_pin = pin_entry.get()
        if guessed_pin == current_pin:
            result_label.config(text="Correct! Well done!")
        else:
            result_label.config(text="Incorrect. Try again!")

    # Create the main window
    root = tk.Tk()
    root.title("The Fun Window")

    # Add a label to display the random choice
    choice_label = tk.Label(root, text="", font=("Helvetica", 16))
    choice_label.pack(pady=10)

    # Add a button that makes a random choice
    random_choice_button = tk.Button(root, text="Random Choice", command=on_random_choice_button_click)
    random_choice_button.pack(pady=10)

    # Add a label to display the 8-digit code
    code_label = tk.Label(root, text="", font=("Helvetica", 16))
    code_label.pack(pady=10)

    # Add a button that generates an 8-digit code
    generate_code_button = tk.Button(root, text="Generate 4-digit Code", command=on_generate_code_button_click)
    generate_code_button.pack(pady=10)

    # Add an entry for guessing the PIN
    pin_entry = tk.Entry(root, font=("Helvetica", 16))
    pin_entry.pack(pady=10)

    # Add a button to submit the guess
    guess_button = tk.Button(root, text="Guess the 3-digit PIN", command=on_guess_button_click)
    guess_button.pack(pady=10)

    # Add a label to display the result of the guess
    result_label = tk.Label(root, text="", font=("Helvetica", 16))
    result_label.pack(pady=10)

    # Generate a random PIN to guess
    current_pin = ''.join(random.choices('0123456789', k=3))

    # Run the Tkinter main loop
    root.mainloop()
