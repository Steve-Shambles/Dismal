"""
Dismal V1
A simple desktop GUI to create a disposable email address and go to the inbox,

By Steve Shambles Oct 2018, Nov 2019, Feb 2021 and april 2023.

Dependants:
pip3 install awesometkinter
pip3 install Pillow
pip3 install pyperclip

files required, in same location as this file:
dismal_logov2.png
dismal_help.txt

icons folder:
about-16x16.ico
blog-16x16.ico
exit-16x16.ico
help-16x16.ico
mguy-16x16.ico
clipb-16x16.ico
"""
import os
from random import randint, choice
import string
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import webbrowser as web

import awesometkinter as atk
from PIL import Image, ImageTk
import pyperclip


root = tk.Tk()
root.title('Dismal V1. April 2023')
root.resizable(False, False)
root.config(background=atk.DEFAULT_COLOR)
root.eval('tk::PlaceWindow . Center')

s = ttk.Style()
s.theme_use('default')
BASE_URL = 'https://www.mailinator.com/v4/public/inboxes.jsp?to='
BASE_EMAIL = '@mailinator.com'


try:
    # pre-load icons for drop-down menu.
    help_icon = ImageTk.PhotoImage(file='icons/help-16x16.ico')
    about_icon = ImageTk.PhotoImage(file='icons/about-16x16.ico')
    github_icon = ImageTk.PhotoImage(file='icons/github-16x16.ico')
    exit_icon = ImageTk.PhotoImage(file='icons/exit-16x16.ico')
    mguy_icon = ImageTk.PhotoImage(file='icons/mguy-16x16.ico')
    clipb_icon = ImageTk.PhotoImage(file='icons/clipb-16x16.ico')
    donate_icon = ImageTk.PhotoImage(file='icons/donation-16x16.ico')
except FileNotFoundError as e:
    messagebox.showerror('file Error:', 'Icon or icons are missing\n'
                                        'Please re-install.')
    root.destroy()
    sys.exit()


def load_emails():
    """ Load in text file containing previously made emails. """
    if os.path.isfile('dismal-lb.txt'):
        with open('dismal-lb.txt', 'r') as f:
            emails = f.read().splitlines()
            if emails:
                for x in range(len(emails)):
                    list_box.insert('end', emails[x])
    else:
        with open('dismal-lb.txt', 'w+') as _:
            pass


def clk_but():
    """ Button was clicked so create Email address. """
    # Get contents of entry box.
    e_name = entry_box.get()

    if not e_name:
        # If no username entered, create random one.
        allchar = string.ascii_lowercase + string.digits
        e_name = ''.join(choice(allchar) for x in range(randint(6, 8)))

    # strip out any spaces in name.
    e_name = e_name.replace(" ", "")
    # Construct email address.
    email_address = e_name+BASE_EMAIL
    # Copy email address to clipboard.
    pyperclip.copy(email_address)
    # Clear entry box and insert new address in listbox.
    entry_box.delete(0, tk.END)
    list_box.insert('end', email_address)

    # Append new email address to text file for reloding next.
    with open('dismal-lb.txt', 'a') as contents:
        save_it = str(email_address+'\n')
        contents.write(save_it)

    ask_yn = messagebox.askyesno('Info', 'your new email address is\n\n'
                                 + str(email_address)+'\n\n'
                                 'The address has been copied\n'
                                 'to your clipboard.\n\n'
                                 'Click "Yes" to go to your inbox now,\n')
    if not ask_yn:
        entry_box.focus()
        return

    # Open new adresses inbox in browser.
    web.open(BASE_URL+e_name)
    # Place cursor inside entry box awaiting next creation.
    entry_box.focus()


def about_menu():
    """ About program. """
    messagebox.showinfo('About',
                        'Dismal V1\nFreeware\nBy Steve Shambles.\n'
                        'Last updated April 2023.')


def github():
    """ Visit my GitHub page for lots of source code. """
    web.open('https://github.com/Steve-Shambles?tab=repositories')


def donate():
    """Open PayPal donation page."""
    web.open('https://paypal.me/photocolourizer')


def go_mailinator():
    """ Visit mailinator website. """
    web.open('https://www.mailinator.com')
    entry_box.focus()


def popup(event):
    """ On right click display popup menu at mouse position. """
    rc_menu.post(event.x_root, event.y_root)


def copy_em_adr():
    """ Called when Copy to clipboard selected from right click menu. """
    try:
        selection = list_box.curselection()
        slctd_adrs = list_box.get(selection[0])
    except IndexError:
        messagebox.showerror('Error:', 'Nothing selected')
        return
    pyperclip.copy(slctd_adrs)
    messagebox.showinfo('Info', slctd_adrs + '\nCopied to clipboard.')
    entry_box.focus()


def delete_all():
    """ Delete all email addresses from listbox and text file. """
    ask_yn = messagebox.askyesno('Question', 'Delete all Email addresses?')
    if not ask_yn:
        return

    # Remove all items from the listbox.
    list_box.delete(0, 'end')
    # Blank the text file.
    with open('dismal-lb.txt', 'w') as _:
        pass

    entry_box.focus()


def delete_em_adr():
    """ Called when delete address is selected from right click menu. """
    # Get the file that is selected in the list box.
    try:
        selection = list_box.curselection()
        slctd_adrs = list_box.get(selection[0])
    except IndexError:
        messagebox.showerror('Error:', 'Nothing selected')
        return

    ask_yn = messagebox.askyesno('Question', 'Delete selected Email?')
    if not ask_yn:
        return

    # Delete email.
    list_box.delete(selection)
    # Remove email from text file by re-opening as a blank file
    # and re-saving with current listbox contents.
    with open('dismal-lb.txt', 'w') as g:
        g.write('\n'.join(list_box.get(0, tk.END)))
        g.write('\n')

    entry_box.focus()


def open_inbox():
    """ Open currently selected email address at malinator.com. """
    try:
        selection = list_box.curselection()
        slctd_adrs = list_box.get(selection[0])
    except IndexError:
        messagebox.showerror('Error:', 'Nothing selected')
        return
    #  Remove @malinator.com from value.
    value2 = slctd_adrs.replace('@mailinator.com', '')
    eml_adrs = BASE_URL+value2
    web.open(eml_adrs)
    entry_box.focus()


def open_in_txt():
    """ Open the text file that stores the list of emails. """
    web.open('dismal-lb.txt')
    entry_box.focus()


def help_me():
    """ Opens a help, using systems default text viewer. """
    web.open('dismal_help.txt')
    entry_box.focus()


def exit_app():
    """ Don't go.I love you and want to have your children, I'm rich too!. """
    ask_yn = messagebox.askyesno('Question', 'Confirm exit Dismal?')
    if not ask_yn:
        return
    root.destroy()
    sys.exit()


# Set up frames for GUI.
logo_frame = tk.Frame(root)
logo_frame.grid(padx=8, pady=8)

main_frame = atk.Frame3d(root)
main_frame.grid(padx=10, pady=10)

listbox_frame = atk.Frame3d(root)
listbox_frame.grid(padx=10, pady=10)

# Load and display logo.
if not os.path.isfile('dismal_logov2.png'):
    messagebox.showerror('File Error:', 'dismal_logov2.png\nIs missing.')
    root.destroy()
    sys.exit()

logo_image = Image.open('dismal_logov2.png')
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(logo_frame, image=logo_photo)
logo_label.logo_image = logo_photo
logo_label.grid(padx=2, pady=2, row=0, column=0)

# Create entry box.
entry_box = tk.Entry(main_frame, bd=3, bg='slategray1')
entry_box.grid(sticky=tk.W+tk.E, padx=5, pady=5)

# Create Email button.
create_mail_btn = atk.Button3d(main_frame, text='Create Email',
                               command=clk_but)
create_mail_btn.grid(pady=15, padx=15)

# Listbox with scrollbars.
list_box = tk.Listbox(
    master=listbox_frame,
    selectmode='single',
    width=25,
    height=8,
    bg='cornflower blue',
    fg='black')

sbar_vert = tk.Scrollbar(listbox_frame, orient='vertical')
sbar_vert.pack(side=tk.RIGHT, fill=tk.Y)
list_box.configure(yscrollcommand=sbar_vert.set)
sbar_vert.configure(command=list_box.yview)

sbar_hor = tk.Scrollbar(listbox_frame, orient='horizontal')
sbar_hor.pack(side=tk.BOTTOM, fill=tk.X)
list_box.configure(xscrollcommand=sbar_hor.set)
sbar_hor.configure(command=list_box.xview)

list_box.pack()

# Bind mouse right click to listbox for right-click pop up menu.
list_box.bind('<Button-3>', popup)

# Create the popup menu.
rc_menu = tk.Menu(root, tearoff=0)

rc_menu.add_command(label='Open inbox',
                    command=open_inbox)
rc_menu.add_command(label='Copy address to clipboard',
                    command=copy_em_adr)
rc_menu.add_separator()
rc_menu.add_command(label='Delete this address',
                    command=delete_em_adr)
rc_menu.add_command(label='Delete all addresses',
                    command=delete_all)
rc_menu.add_separator()
rc_menu.add_command(label='Open all addresses in a text file',
                    command=open_in_txt)
rc_menu.add_command(label='Visit mailinator.com', compound='left',
                    image=mguy_icon,
                    command=go_mailinator)


# Drop-down menu.
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Menu', menu=file_menu)
file_menu.add_command(label='Help', compound='left',
                      image=help_icon, command=help_me)
file_menu.add_command(label='About', compound='left',
                      image=about_icon, command=about_menu)
file_menu.add_command(label='Source Code', compound='left',
                      image=github_icon, command=github)
file_menu.add_command(label='Donate', compound='left',
                      image=donate_icon, command=donate)
file_menu.add_separator()
file_menu.add_command(label='Exit', compound='left',
                      image=exit_icon, command=exit_app)
root.config(menu=menu_bar)

# If help file missing disable help item in drop-down menu.
check_file = os.path.isfile('dismal_help.txt')
if not check_file:
    file_menu.entryconfig(0, state=DISABLED)


entry_box.focus()
load_emails()

root.protocol("WM_DELETE_WINDOW", exit_app)

root.mainloop()
