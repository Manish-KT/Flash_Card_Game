from tkinter import *
import random
import pandas

time = None
BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv("words_to_learn.csv")

except FileNotFoundError:
    data = pandas.read_csv("csv files/french_words.csv")

french_wordlist = data.French.tolist()
english_wordlist = data.English.tolist()
unknown_wordlist = {
    "French": french_wordlist,
    "English": english_wordlist
}

index = None
wordlist = data.index.tolist()


# ---------------------------- SAVING DATA ------------------------------- #
def known_words():
    french_wordlist.remove(french_wordlist[index])
    english_wordlist.remove(english_wordlist[index])

    new_data = pandas.DataFrame(unknown_wordlist)
    new_data.to_csv("csv files/words_to_learn")
    french_word()


# ---------------------------- RANDOM WORD ------------------------------- #

def english_word():
    global data, index, time
    random_english_word = data.loc[index, "English"]
    data.drop(index, axis=0, inplace=True)
    canvas.create_image(400, 290, image=back_img)
    french_label.config(text="English", bg="#94c3ab", fg="white")
    f_word.config(text=random_english_word, bg="#94c3ab", fg="white")
    window.after_cancel(time)


def french_word():
    global data, index, time
    index = random.choice(wordlist)
    random_french_word = data.loc[index, "French"]

    canvas.create_image(400, 290, image=front_img)
    french_label.config(text="French", bg="white", fg="black")
    f_word.config(text=random_french_word, font=("Ariel", 60, "bold"), bg="white", fg="black")
    f_word.place(relx=0.5, rely=0.5, anchor=CENTER)
    time = window.after(3000, func=english_word)


def remove():
    start_button.destroy()
    right_button.config(state=NORMAL)
    wrong_button.config(state=NORMAL)
    french_word()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flash Card Game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
canvas = Canvas(width=800, height=600, highlightthickness=0, bg=BACKGROUND_COLOR)

# images
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")

canvas.create_image(400, 290, image=front_img)
canvas.grid(row=0, column=0, columnspan=2)

# labels
french_label = Label(text="", font=("Ariel", 40, "italic"), background="White", highlightthickness=0)
french_label.place(x=310, y=125)
f_word = Label(text="", font=("Ariel", 30, "bold"), background="White", highlightthickness=0)
f_word.place(relx=0.5, rely=0.4, anchor=CENTER)

# Buttons
right_button = Button(image=right_img, highlightthickness=0, command=known_words, state=DISABLED)
right_button.grid(row=1, column=1)
wrong_button = Button(image=wrong_img, highlightthickness=0, command=french_word, state=DISABLED)
wrong_button.grid(row=1, column=0)
start_button = Button(text="Start", width=5, height=1, font=("Ariel", 30, "bold"), command=remove)
start_button.place(relx=0.5, rely=0.4, anchor=CENTER)

window.mainloop()
