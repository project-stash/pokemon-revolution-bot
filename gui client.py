import tkinter as tk                     
from tkinter import ttk
from tkinter import Button 
from tkinter import Entry
import json
import subprocess
import os,time,threading
from pokemonlist import pokemon_list
file_path = "user_data.json"
user_data = {}
def submit_username():
    username = entry.get()
    password = entry2.get()
    user_data[username] = password
    if username == "":
        load_user_data()
        for key,value in user_data.items():
            username = key
            password = value
    remove_username()
    if username !="":
        save_user_data()
    tabControl.forget(tab1)
    subprocess.Popen(["python", "pokemon.py", username, password])
    
def remove_username():
    username = entry.get()
    entered_password = entry2.get()

    # Check if the username exists in the dictionary
    if username in user_data:
        # Check if the entered password matches the saved password
        if entered_password != user_data[username]:
            # Remove username from the dictionary
            del user_data[username]

            # Save user data to the file
            save_user_data()
def save_user_data():
    # Save user data to the file
    with open(file_path, 'w') as file:
        json.dump(user_data, file)
def load_user_data():
    # Load user data from the file
    try:
        with open(file_path, 'r') as file:
            user_data.update(json.load(file))
    except FileNotFoundError:
        pass  # Ignore if the file is not found

def start_program():
    global Continue,Stop
    with open("stop.txt", "w") as signal_file:
        signal_file.write("not")
    with open("signal.txt", "w") as signal_file:
        signal_file.write("pressed")
    Continue = ttk.Button(tab2, text="Continue", command=continue_program)
    Continue.grid(row=20, column=0, columnspan=5, pady=100, padx=10, sticky=tk.S)
    Stop = ttk.Button(tab2, text="Stop", command=stop_program)
    Stop.grid(row=20, column=1, columnspan=5, pady=100, padx=10, sticky=tk.S)
    with open("pokemon_List.json", "w") as signal_file:
        json.dump(pokemon_hunt_list, signal_file)
    with open("dodgelist.json", "w") as signal_file:
        json.dump(DodgeList, signal_file)
    add_Pokemon1.config(state="disabled")
    Continue.config(state="disabled")
    Stop.config(state="disabled")
    add_Pokemon2.config(state="disabled")
    remove_Pokemon1.config(state="disabled")
    remove_Pokemon2.config(state="disabled")
    startProgram.destroy()
    signal_file = "return.txt"
    while not os.path.exists(signal_file):
       time.sleep(1)
    os.remove(signal_file)
    program_thread = threading.Thread(target=run_program)
    program_thread.start()
def run_program():
    add_Pokemon1.config(state=tk.NORMAL)
    Stop.config(state=tk.NORMAL)
    Continue.config(state=tk.NORMAL)
    add_Pokemon2.config(state=tk.NORMAL)
    remove_Pokemon1.config(state=tk.NORMAL)
    remove_Pokemon2.config(state=tk.NORMAL)
def stop_program():
    with open("stop.txt", "w") as signal_file:
        signal_file.write("pressed")
    root.destroy()
def add_pokemon():
    pokemon_name = entry_var.get()
    if pokemon_name in pokemon_list and pokemon_name not in pokemon_hunt_list and pokemon_name not in DodgeList:
        pokemon_hunt_list.append(pokemon_name)
        update_pokemon_list()
    entry_var.set("")

def continue_program():
    with open("signal.txt", "w") as signal_file:
        signal_file.write("pressed")
    with open("pokemon_List.json", "w") as signal_file:
        json.dump(pokemon_hunt_list, signal_file)
    with open("dodgelist.json", "w") as signal_file:
        json.dump(DodgeList, signal_file)
    Continue.config(state="disabled")
    Stop.config(state="disabled")
    add_Pokemon1.config(state="disabled")
    add_Pokemon2.config(state="disabled")
    remove_Pokemon1.config(state="disabled")
    remove_Pokemon2.config(state="disabled")
    signal_file = "return.txt"
    while not os.path.exists(signal_file):
        time.sleep(1)
    os.remove(signal_file)
    program_thread = threading.Thread(target=run_program)
    program_thread.start()
    
def add_pokemon2():
    pokemon_name = entry_var2.get()
    if pokemon_name in pokemon_list and pokemon_name not in DodgeList and pokemon_name not in pokemon_hunt_list:
        DodgeList.append(pokemon_name)
        update_pokemon_list2()
    entry_var2.set("")

def update_pokemon_list():
    # Clear and update the Pokemon list in the text widget
    text_widget["state"] = tk.NORMAL
    if text_widget.get(1.0, tk.END) != "":
        text_widget.delete(1.0, tk.END)
    
    for pokemon in pokemon_hunt_list:
        text_widget.insert(tk.END, f"{pokemon}\n")
    text_widget["state"] = tk.DISABLED

def update_pokemon_list2():
    # Clear and update the Pokemon list in the text widget
    text_widget2["state"] = tk.NORMAL
    if text_widget2.get(1.0, tk.END) != "":
        text_widget2.delete(1.0, tk.END)
    
    for pokemon in DodgeList:
        text_widget2.insert(tk.END, f"{pokemon}\n")
    text_widget2["state"] = tk.DISABLED     
   
def on_select_combobox(event=None):
    # Update the entry with the selected value from the combobox
    entry_var.set(combo.get())

    # Get the current value in the entry
    value = entry_var.get().lower()

    # Find matches from the predefined list (pokemon_list)
    matches = [item for item in pokemon_list if item.lower().startswith(value)]

    # Update the combobox dropdown list with matching items
    combo["values"] = matches

    if matches: 
        combo.lift()  # Show the dropdown list

def on_select_combobox1(event=None):
    # Update the entry with the selected value from the combobox
    entry_var1.set(combo1.get())

    # Get the current value in the entry
    value1 = entry_var1.get().lower()

    # Find matches from the predefined list (pokemon_list)
    matches1 = [item for item in pokemon_hunt_list if item.lower().startswith(value1)]

    # Update the combobox dropdown list with matching items
    combo1["values"] = matches1

    if matches1: 
        combo1.lift()  # Show the dropdown list

def on_select_combobox2(event=None):
    # Update the entry with the selected value from the combobox
    entry_var2.set(combo2.get())

    # Get the current value in the entry
    value2 = entry_var2.get().lower()

    # Find matches from the predefined list (pokemon_list)
    matches2 = [item for item in pokemon_list if item.lower().startswith(value2)]

    # Update the combobox dropdown list with matching items
    combo2["values"] = matches2

    if matches2: 
        combo2.lift()  # Show the dropdown list
        
def on_select_combobox3(event=None):
    # Update the entry with the selected value from the combobox
    entry_var3.set(combo3.get())

    # Get the current value in the entry
    value3 = entry_var3.get().lower()

    # Find matches from the predefined list (pokemon_list)
    matches3 = [item for item in DodgeList if item.lower().startswith(value3)]

    # Update the combobox dropdown list with matching items
    combo3["values"] = matches3

    if matches3: 
        combo3.lift()  # Show the dropdown list

def remove_pokemon():
    pokemon_name1 = entry_var1.get()
    if pokemon_name1 in pokemon_hunt_list:
        pokemon_hunt_list.remove(pokemon_name1)
        update_pokemon_list()
    entry_var1.set("")
    
def remove_pokemon2():
    pokemon_name2 = entry_var3.get()
    if pokemon_name2 in DodgeList:
        DodgeList.remove(pokemon_name2)
        update_pokemon_list2()
    entry_var3.set("")
def main(): 
    global entry,entry2,tab1, tabControl,pokemon_hunt_list,text_widget,entry_var,combo,addpokemon1,DodgeList,entry_var1,combo1,root
    global entry_var2,combo2,text_widget2,entry_var3,combo3,tab2,startProgram,add_Pokemon1,remove_Pokemon1,add_Pokemon2,remove_Pokemon2
    pokemon_hunt_list = []
    DodgeList=[]
    addpokemon1=""
    root = tk.Tk() 
    root.title("Tab Widget") 
    root.geometry("500x500")
    tabControl = ttk.Notebook(root) 

    tab1 = ttk.Frame(tabControl) 
    tab2 = ttk.Frame(tabControl) 
  
    tabControl.add(tab1, text ='Login') 
    tabControl.add(tab2, text ='land hunting') 
    tabControl.pack(expand = 1, fill ="both") 
    label1 = ttk.Label(tab1, text="Enter your username:")
    label1.pack(pady=10)
    entry = tk.Entry(tab1)
    entry.pack(pady=10)
    label2 = ttk.Label(tab1, text="Enter your password:")
    label2.pack(pady=10)
    entry2 = tk.Entry(tab1)
    entry2.pack(pady=10)
    submit_button1 = ttk.Button(tab1, text="Login", command=submit_username)
    submit_button1.pack(pady=10)
    ##pokemon hunting
    label3 = ttk.Label(tab2, text="pokemonHuntList:")
    label3.grid(row=0, column=0, pady=10, padx=10, sticky=tk.NW)

    text_widget = tk.Text(tab2, height=5, width=20, state=tk.DISABLED)
    text_widget.grid(row=1, column=0, pady=10, padx=10, sticky=tk.W)

    label4 = ttk.Label(tab2, text="DodgeList:")
    label4.grid(row=3, column=0, pady=10, padx=10, sticky=tk.NW)
    text_widget2 = tk.Text(tab2, height=5, width=20, state=tk.DISABLED)
    text_widget2.grid(row=4, column=0, pady=10, padx=10, sticky=tk.W)
    
    entry_var = tk.StringVar()
    combo = ttk.Combobox(tab2, textvariable=entry_var, postcommand=on_select_combobox)
    combo.grid(row=1, column=3, pady=10)
    combo["values"] = pokemon_hunt_list
    combo.bind("<<ComboboxSelected>>", on_select_combobox)
    
    add_Pokemon1 = ttk.Button(tab2, text="Add_Pokemon",command=add_pokemon)
    add_Pokemon1.grid(row=2, column = 3)
    
    entry_var1 = tk.StringVar()
    combo1 = ttk.Combobox(tab2, textvariable=entry_var1, postcommand=on_select_combobox1)
    combo1.grid(row=1, column=4, pady=10)
    combo1["values"] = pokemon_hunt_list
    combo1.bind("<<ComboboxSelected>>", on_select_combobox1)
    
    remove_Pokemon1 = ttk.Button(tab2, text="Remove_Pokemon",command = remove_pokemon)
    remove_Pokemon1.grid(row=2, column = 4)
    
    entry_var2 = tk.StringVar()
    combo2 = ttk.Combobox(tab2, textvariable=entry_var2, postcommand=on_select_combobox2)
    combo2.grid(row=4, column=3, pady=10)
    combo2["values"] = DodgeList
    combo2.bind("<<ComboboxSelected>>", on_select_combobox2)
    
    add_Pokemon2 = ttk.Button(tab2, text="Add_Pokemon",command=add_pokemon2)
    add_Pokemon2.grid(row=5, column = 3)
    
    entry_var3 = tk.StringVar()
    combo3 = ttk.Combobox(tab2, textvariable=entry_var3, postcommand=on_select_combobox3)
    combo3.grid(row=4, column=4, pady=10)
    combo3["values"] = DodgeList
    combo3.bind("<<ComboboxSelected>>", on_select_combobox3)
    
    remove_Pokemon2 = ttk.Button(tab2, text="Remove_Pokemon",command = remove_pokemon2)
    remove_Pokemon2.grid(row=5, column = 4)
    startProgram = ttk.Button(tab2, text="start Program", command=start_program)
    startProgram.grid(row=20, column=0, columnspan=5, pady=100, padx=10, sticky=tk.S)
    root.mainloop()

if __name__ == "__main__":
    main()