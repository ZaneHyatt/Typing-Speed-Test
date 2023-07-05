from tkinter import *
import openai
import math
import os
from dotenv import load_dotenv

load_dotenv()

BACKGROUND = "#635985"
FONT_COLOR = "#E9F8F9"
FONT_NAME = "Courier"

openai.api_key = os.getenv("OPENAIKEY")

message_history = []
char_count = 0
timer = None
counter = 0
incorrect = 0
word_count = 0


def chat(inp, role="user"):
    message_history.append({"role": role, "content": inp})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history,
    )

    reply_content = completion["choices"][0]["message"]["content"]
    message_history.append({"role": "assistant", "content": f"{reply_content}"})
    return reply_content


prompt = "Give me a random 3 paragraph text about an random informative topic for a type speed test"
text = str(chat(prompt))
text_list = list(text)


def key_press(event):
    global counter
    global incorrect
    global word_count
    key = event.char
    print(key)
    if text_list[counter] == key:
        print("correct")
        counter += 1
        T.tag_config("start", foreground="green", background="#393053")
        T.tag_add("start", "1.0", f"1.{str(counter)}")
        if key == " ":
            word_count += 1
            word_canvas.itemconfig(word_text, text=str(word_count))
    else:
        incorrect += 1
        incorrect_canvas.itemconfig(incorrect_text, text=str(incorrect))


def start_timer(event):
    window.bind('<Key>', key_press)
    count_down(60)


def count_down(count):
    global incorrect
    global word_count

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    timer_canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count == 0:
        T.destroy()
        incorrect_canvas.destroy()
        word_canvas.destroy()
        start_button.destroy()
        stats = Label(window, text=f"You typed {word_count} words per minute on average\nYou got {incorrect} incorrect",
                      bg=BACKGROUND, fg=FONT_COLOR, font=(FONT_NAME, 35, "bold"))
        stats.pack()
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)


window = Tk()
window.title("Typing Speed Test")
window.config(padx=100, pady=50, bg=BACKGROUND)

incorrect_canvas = Canvas(width=50, height=50, bg=BACKGROUND, highlightthickness=0)
incorrect_text = incorrect_canvas.create_text(25, 25, text=str(incorrect), fill=FONT_COLOR, font=(FONT_NAME, 40, "bold"))
incorrect_canvas.pack()

word_canvas = Canvas(width=50, height=50, bg=BACKGROUND, highlightthickness=0)
word_text = word_canvas.create_text(25, 25, text=str(word_count), fill=FONT_COLOR, font=(FONT_NAME, 40, "bold"))
word_canvas.pack()

timer_canvas = Canvas(width=100, height=50, bg=BACKGROUND, highlightthickness=0)
timer_text = timer_canvas.create_text(50, 25, text="00:00", fill=FONT_COLOR, font=(FONT_NAME, 35, "bold"))
timer_canvas.pack()

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.pack()

T = Text(window, height=50, width=50, wrap=WORD, font=(FONT_NAME, 32), background=BACKGROUND, fg=FONT_COLOR)
T.insert(END, text)
T.pack()

window.bind('<Up>', start_timer)

window.mainloop()
