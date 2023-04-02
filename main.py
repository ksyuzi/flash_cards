import random
from tkinter import *

import pandas

BACKGROUND_COLOR = "#B1DDC6"
LANG_TITLE_FORMAT = ('Ariel', 40, 'italic')
WORD_TEXT_FORMAT = ('Ariel', 60, 'bold')

random_words = {}
all_words = {}


def generate_random_word():
    global random_words, flip_timer
    window.after_cancel(flip_timer)
    random_words = random.choice(all_words)
    canvas.itemconfig(word, text=random_words['French'], fill="black")
    canvas.itemconfig(language, text='French', fill="black")
    canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(language, fill="white", text="English")
    canvas.itemconfig(word, fill="white", text=random_words['English'])
    canvas.itemconfig(card_background, image=card_back)


def check_button_pressed():
    global random_words
    all_words.remove(random_words)
    all_words_data = pandas.DataFrame(all_words)
    all_words_data.to_csv("./data/words_to_learn.csv")

    new_data = pandas.DataFrame(random_words, index=[0])
    new_data.to_csv("./data/learned words.csv")
    generate_random_word()


# Reading the CSV file
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    all_words = pandas.DataFrame(original_data).to_dict(orient='records')
else:
    all_words = pandas.DataFrame(data).to_dict(orient='records')

#  Performing UI setup
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_background = canvas.create_image(400, 263, image=card_front)
canvas.grid(row=0, column=0, columnspan=2)

card_back = PhotoImage(file="./images/card_back.png")

language = canvas.create_text(400, 150, text="", font=LANG_TITLE_FORMAT)
word = canvas.create_text(400, 263, text="word", font=WORD_TEXT_FORMAT)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=generate_random_word)
wrong_button.grid(column=0, row=1)

right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=check_button_pressed)
right_button.grid(column=1, row=1)

# Generating a random word and showing it to the user
generate_random_word()
window.mainloop()
