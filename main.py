import tkinter
from tkinter import END, messagebox
from random import choice, randint, shuffle
import pyperclip
import json

OLIVE = "#D2E3C8"
WHITE = "#FFF7F1"
SAGE = "#294B29"
FONT = ('Constantia', 12, 'bold')


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web = website_entry.get().title()
    user = username_entry.get()
    pss = password_entry.get()
    new_data = {
        web: {
            "email": user,
            "password": pss,
        }
    }

    if len(web) == 0 or len(pss) == 0 or len(user) == 0:
        messagebox.showinfo(title="Ooopppss!!", message="Please don't leave any fields empty!!")
    else:
        is_ok = messagebox.askokcancel(title=web, message=f"These are the details entered: \nEmail: {user} "
                                                          f"\nPassword: {pss} \nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                username_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website_name = website_entry.get().title()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website_name in data:
            email = data[website_name]["email"]
            password = data[website_name]["password"]
            messagebox.showinfo(title=website_name, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website_name} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title("Password Manager Application")
window.minsize(width=340, height=100)
window.config(padx=50, pady=50, bg=OLIVE)

canvas = tkinter.Canvas(width=200, height=200, bg=OLIVE, highlightthickness=0)
img = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

website = tkinter.Label(text="Website: ", bg=OLIVE, font=FONT, fg=SAGE)
website.grid(column=0, row=1)

username = tkinter.Label(text="Email/Username: ", bg=OLIVE, font=FONT, fg=SAGE)
username.grid(column=0, row=2)

pswrd = tkinter.Label(text="Password: ", bg=OLIVE, font=FONT, fg=SAGE)
pswrd.grid(column=0, row=3)

website_entry = tkinter.Entry(width=35)
website_entry.grid(column=1, row=1, sticky=tkinter.W)
website_entry.focus()

username_entry = tkinter.Entry(width=35)
username_entry.grid(column=1, row=2, columnspan=2, sticky=tkinter.W)

password_entry = tkinter.Entry(width=21)
password_entry.grid(column=1, row=3, sticky=tkinter.W)

search_button = tkinter.Button(text="Search", width=13, command=find_password, font=FONT, fg=SAGE)
search_button.grid(row=1, column=2)
search_button.config(padx=18)

generate_button = tkinter.Button(text="Generate password", bg=WHITE, command=generate_password, font=FONT, fg=SAGE)
generate_button.grid(column=2, row=3)
generate_button.config(padx=10)

add_button = tkinter.Button(text="Add", bg=WHITE, command=save, font=FONT, fg=SAGE)
add_button.grid(column=1, row=4, columnspan=2, sticky=tkinter.W)
add_button.config(width=34)

window.mainloop()
