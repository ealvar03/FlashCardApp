from tkinter import *
import pandas
import random
import os.path

BACKGROUND_COLOR = "#B1DDC6"


# ----------- FUNCTIONALITY ----------- #

file_exists = os.path.isfile("data/words_to_learn.csv")
if file_exists:
    data = pandas.read_csv("data/words_to_learn.csv")
else:
    data = pandas.read_csv("data/french_words.csv")
dict_data = data.to_dict(orient="records")
current_card = {}


def select_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(dict_data)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=flash_card_front)
    flip_timer = window.after(3000, func=flip_card)


def is_known():
    dict_data.remove(current_card)
    select_word()
    missing_words = pandas.DataFrame(dict_data)
    missing_words.to_csv("data/words_to_learn.csv", index=False)


def flip_card():
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_image, image=flash_card_back)


# --------------- GUI ----------------- #

window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Buttons
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=is_known)
right_button.grid(column=1, row=1)
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=select_word)
wrong_button.grid(column=0, row=1)

# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
flash_card_front = PhotoImage(file="images/card_front.png")
flash_card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=flash_card_front)
language = canvas.create_text(400, 150, text="", fill="black", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="", fill="black", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

select_word()

window.mainloop()
