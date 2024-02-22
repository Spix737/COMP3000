from tkinter import *

root = Tk()
root.title('Catan GUI')
root.iconbitmap('assets/cstm.it3 cns')

canvas = Canvas()
# Creating a label widget
myLabel = Label(root, text='Hello wurld')
myButton = Button(root, text='click me', state=DISABLED, padx='50px', command=quit)

n1 = canvas.create_oval(10, 10, 80, 80, outline = "black", fill = "white",width = 2)

# Shoving it onto the screen
myLabel.grid(row=0, column=14)
myButton.grid(row=1, column=0)


root.mainloop()

# 27 g board

# idk rest of gui, another 37 rest of? 64 total

