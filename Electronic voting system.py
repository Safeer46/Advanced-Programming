import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import matplotlib.pyplot as plt


conn = sqlite3.connect('mydb.sqlite')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS voting (
        id INTEGER ,
        citizen_id varchar,
        vote TEXT NOT NULL,
        status integer
    )
''')


def load_chart():
    data = []
    x = ['Christian Democratic Union', 'Social Democratic Party of Germany', 'The Left', 'Alliance 90/The Greens', 'Alternative for Germany', 'Free Democratic Party', 'Die PARTEI', 'Animal Protection Party']
    for i in range(1,9):
        cursor.execute(f"select count(vote) from voting where id = '{str(i)}' and status = 1")
        data.insert(i-1, cursor.fetchone()[0])
    print(data)
    

    ax.clear()
    # try:
        
    # except Exception as e:
    #     ex=e
    ax.bar(x, data)
    ax.set_xticks(x)
    ax.set_xticklabels(x, rotation=45, ha='right')
    ax.set_ylabel('Votes Casted')
    ax.set_title('Voting Chart')
    canvas.draw()
    # Adjust subplot margins to ensure labels are fully visible
    plt.subplots_adjust(bottom=0.2)  # Increase bottom margin as needed

    # Show the plot
    plt.tight_layout()
    # plt.show()

# Create a function to update the bar chart based on user input
def update_chart():
    # print("entry1: ",entry1.get())
    # data = [int(entry1.get()), int(entry2.get()), int(entry3.get())]
    # print("Party: ", party.current())
    # return
    
    cursor.execute(f"select count(id) from voting where citizen_id = '{str(entry1.get())}'")
    if int(cursor.fetchone()[0]) >= 1:
        messagebox.showerror("Voting Error", "Vote Already Casted.")
        return
    
    if party.current() == -1:
        messagebox.showerror("Voting Error", "Please select your favourite Party to cast vote.")
        return
        
    
    cursor.execute(f"insert into voting (id, citizen_id, vote, status) values ('{str(party.current()+1)}', '{str(entry1.get())}', '1', '1')")
    conn.commit()
    
    load_chart()
    
    

# Create the main window
root = tk.Tk()
root.title("German Voting System")
root.geometry("800x600")

# Create form elements
frame = ttk.Frame(root, padding=10)
frame.grid(column=0, row=0, sticky = tk.W)


label1 = ttk.Label(frame, text="Enter your German ID Card No.")
entry1 = ttk.Entry(frame)
label2 = ttk.Label(frame, text="Select Party to Case Vote.")
n = tk.StringVar()
party = ttk.Combobox(frame, width = 27, textvariable = n)
party['values'] = ('Christian Democratic Union', 
                    'Social Democratic Party of Germany', 
                    'The Left', 
                    'Alliance 90/The Greens', 
                    'Alternative for Germany', 
                    'Free Democratic Party', 
                    'Die PARTEI', 
                    'Animal Protection Party')
party.current()

button = ttk.Button(frame, text="Cast Vote", command=update_chart)
# button.place(x=35, y=5)
# Create Matplotlib figure and canvas
# fig = Figure(figsize=(8, 5), dpi=100)
# ax = fig.add_subplot(111)
fig, ax = plt.subplots(figsize=(8, 5))  # Increase figure size to accommodate longer labels



canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(column=0, row=6, columnspan=5)
# canvas.get_tk_widget().pack()

# Place form elements on the grid
label1.grid(column=0, row=0)
label2.grid(column=0, row=1)
entry1.grid(column=1, row=0)
party.grid(column=1, row=1)
button.grid(column=0, row=4, columnspan=2)

# Initialize the chart with default values
# update_chart()
load_chart()

# Start the Tkinter main loop
root.mainloop()
