from tkinter import *
from PIL import Image, ImageTk
import action
import spech_to_text
import sqlite3
import pandas as pd
import os

def insert_conversation(user_input, bot_output):
    # Insert into SQLite database
    conn = sqlite3.connect('virtual_assistant.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO conversations (user_input, bot_output) VALUES (?, ?)
    ''', (user_input, bot_output))
    conn.commit()
    conn.close()
    
    # Append to CSV file
    file_path = 'va.csv'
    
    # Check if the file exists
    if os.path.isfile(file_path):
        try:
            # Load existing file
            df_existing = pd.read_csv(file_path, encoding='utf-8')
        except (UnicodeDecodeError, pd.errors.ParserError):
            # If there's an error reading the CSV, create a new DataFrame
            df_existing = pd.DataFrame(columns=['User Input', 'Bot Output'])
    else:
        # Create a new DataFrame if the file does not exist
        df_existing = pd.DataFrame(columns=['User Input', 'Bot Output'])
    
    # Create new DataFrame for the new conversation
    df_new = pd.DataFrame({'User Input': [user_input], 'Bot Output': [bot_output]})
    
    # Append the new conversation to the existing DataFrame
    df_final = pd.concat([df_existing, df_new], ignore_index=True)
    
    # Write the final DataFrame back to the CSV file
    df_final.to_csv(file_path, index=False, encoding='utf-8')

def User_send():
    send = entry1.get()
    bot = action.Action(send)
    text.insert(END, "Me --> " + send + "\n")
    if bot is not None:
        text.insert(END, "Bot <-- " + str(bot) + "\n")
        insert_conversation(send, bot)
    if bot == "ok sir":
        root.destroy()

def ask():
    ask_val = spech_to_text.spech_to_text()
    bot_val = action.Action(ask_val)
    text.insert(END, "Me --> " + ask_val + "\n")
    if bot_val is not None:
        text.insert(END, "Bot <-- " + str(bot_val) + "\n")
        insert_conversation(ask_val, bot_val)
    if bot_val == "ok sir":
        root.destroy()

def delete_text():
    text.delete("1.0", "end")

root = Tk()
root.geometry("550x675")
root.title("AI Assistant")
root.resizable(False, False)
root.config(bg="#6F8FAF")

# Main Frame
Main_frame = LabelFrame(root, padx=100, pady=7, borderwidth=3, relief="raised")
Main_frame.config(bg="#6F8FAF")
Main_frame.grid(row=0, column=1, padx=55, pady=10)

# Text Label
Text_lable = Label(Main_frame, text="AI Assistant", font=("comic Sans ms", 14, "bold"), bg="#356696")
Text_lable.grid(row=0, column=0, padx=20, pady=10)

# Image
Display_Image = ImageTk.PhotoImage(Image.open("image/assitant.png"))
Image_Lable = Label(Main_frame, image=Display_Image)
Image_Lable.grid(row=1, column=0, pady=20)

# Add a text widget
text = Text(root, font=('Courier 10 bold'), bg="#356696")
text.grid(row=2, column=0)
text.place(x=100, y=375, width=375, height=100)

# Add an entry widget
entry1 = Entry(root, justify=CENTER)
entry1.place(x=100, y=500, width=350, height=30)

# Add a text button1
button1 = Button(root, text="ASK", bg="#356696", pady=16, padx=40, borderwidth=3, relief=SOLID, command=ask)
button1.place(x=70, y=575)

# Add a text button2
button2 = Button(root, text="Send", bg="#356696", pady=16, padx=40, borderwidth=3, relief=SOLID, command=User_send)
button2.place(x=400, y=575)

# Add a text button3
button3 = Button(root, text="Delete", bg="#356696", pady=16, padx=40, borderwidth=3, relief=SOLID, command=delete_text)
button3.place(x=225, y=575)

root.mainloop()