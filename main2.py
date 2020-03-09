from tkinter import *
from tkinter import filedialog
from tkinter import ttk

variable=""
skip=int()
save_folder_path=""
open_folder_path=""
def choose_method(method):
	#Allow user to choose method --> periodic or random
	global variable
	variable=method
def set_skip(nbr):
	pass

def ouvrir():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global open_folder_path
    filename = filedialog.askdirectory()
    open_folder_path.set(filename)

def save_to():
	# Allow user to select a directory and store it in global var
    # called folder_path
    global save_folder_path
    filename = filedialog.askdirectory()
    save_folder_path.set(filename)


fen = Tk()
fen.title('EAF creator')
lab = Label(fen,text='Welcome, please choose a wav folder to be transformed to Eaf. Then choose method; periodic or random.',height=10)

lab.pack()

menubar=Menu(fen)
fen.config(menu=menubar)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Ouvrir",command=ouvrir)
filemenu.add_command(label="Save to",command=save_to)


lab = Label(fen,text='Welcome, please choose a wav folder to be transformed to Eaf. Then choose method; periodic or random.',height=10)

lab.pack()


Button(fen, text='Quit', command=fen.quit).pack(side=RIGHT)
fen.mainloop()