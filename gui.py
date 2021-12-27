import json
import tkinter as tk
from AccountHelper import AccountHelper
from BudgetHelper import BudgetHelper
from RuleHelper import RuleHelper
from Calculate import CalculateHelper

lightgray = "#bababa"
darkgray = "#989898"
titlefont = ("Helvetica", 24)
textfont = ("Helvetica", 18)


root = tk.Tk()
root.geometry("1600x900")
root.configure(background=darkgray)
root.state("zoomed")

root.grid_columnconfigure(0, pad=100)
#root.grid_columnconfigure(1,weight=1)
#root.grid_columnconfigure(2,weight=1)
#root.grid_columnconfigure(3,weight=10)
#root.grid_columnconfigure(4,weight=1)
#root.grid_columnconfigure(5,weight=10)
#root.grid_columnconfigure(6,weight=1)
root.grid_rowconfigure(0, pad=100)
#root.grid_rowconfigure(1,weight=1)


frame_left = tk.Frame(root, width=450, height=850, bg=lightgray)
frame_left.pack_propagate(False) 
frame_left.grid(row=0, column=0, columnspan=3, sticky="ew")

#frame_center = tk.Frame(root, width=450, height=850, bg=lightgray)
#frame_center.pack_propagate(False) 
#frame_center.grid(row=0, column=3, sticky="ew")
#
#frame_right = tk.Frame(root, width=450, height=850, bg=lightgray)
#frame_right.pack_propagate(False) 
#frame_right.grid(row=0, column=5, sticky="ew")
#
#frame_bottom = tk.Frame(root, width=1440, height=100, bg=lightgray)
#frame_bottom.pack_propagate(False) 
#frame_bottom.grid(row=1, column=1, columnspan=5, sticky="ew")


account_label = tk.Label(frame_left, text="Accounts", font=titlefont, bg=lightgray, pady=20, padx=20, bd=5)
#account_label.pack()
account_label.grid(row=0, column=0, sticky="ew")

#budget_label = tk.Label(frame_center, text="Budgets", font=titlefont, bg=lightgray).pack()
#rules_label = tk.Label(frame_right, text="Rules", font=titlefont, bg=lightgray).pack()

#accounts = AccountHelper().itemize()
#accs = []
#for acc in accounts:
#    number = tk.Label(frame_left, text=acc[1], font=textfont, bg=lightgray, anchor="ne")
#    name = tk.Label(frame_left, text=acc[2], font=textfont, bg=lightgray, anchor="ne")
#    balance = tk.Label(frame_left, text=acc[3], font=textfont, bg=lightgray, anchor="ne")
#    budgets = tk.Label(frame_left, text=", ".join(json.loads(acc[4])), font=textfont, bg=lightgray, anchor="ne")
#    number.grid(row=1, column=1, sticky="ew")
#    name.grid(row=1, column=2, sticky="ew")
#    balance.grid(row=1, column=3, sticky="ew")
#    budgets.grid(row=1, column=4, sticky="ew")

    #number.pack()
    #name.pack()
    #balance.pack()
    #budgets.pack()






root.mainloop()










#import tkinter as tk
#
#class Window1:
#    def __init__(self, master):
#        pass
#        # Create labels, entries,buttons
#    def button_click(self):
#        pass
#        # If button is clicked, run this method and open window 2
#
#
#class Window2:
#    def __init__(self, master):
#        #create buttons,entries,etc
#
#    def button_method(self):
#        #run this when button click to close window
#        self.master.destroy()
#
#def main(): #run mianloop 
#    root = tk.Tk()
#    app = Window1(root)
#    root.mainloop()
#
#if __name__ == '__main__':
#    main()