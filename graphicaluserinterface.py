from tkinter import *

root = Tk()
btn_foods = Button(root, text='Foods', padx=20)
btn_meals = Button(root, text='Meals', padx=20)
btn_quit = Button(root, text='Quit', padx=20, command=root.quit)

btn_foods.grid(row=0, column=1)
btn_meals.grid(row=1, column=1)
btn_quit.grid(row=2, column=1)

#root.mainloop()