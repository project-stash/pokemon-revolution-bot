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
pokemonidentifiedList= list()    
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
    # Load user data from the file4d4a
    try:
        with open(file_path, 'r') as file:
            user_data.update(json.load(file))
    except FileNotFoundError:
        pass  # Ignore if the file is not found

def start_program():
    global Continue,Stop
    subprocess.Popen(["python", "pokemon.py"])
    with open("stop.txt", "w") as signal_file:
        signal_file.write("not")
    with open("signal.txt", "w") as signal_file:
        signal_file.write("pressed")
    Continue = ttk.Button(tab2, text="Continue", command=continue_program)
    Continue.grid(row=10, column=0, columnspan=5, pady=100, padx=10, sticky=tk.S)
    Stop = ttk.Button(tab2, text="Stop", command=stop_program)
    Stop.grid(row=10, column=1, columnspan=5, pady=100, padx=10, sticky=tk.S)
    with open("pokemon_List.json", "w") as signal_file:
        json.dump(pokemon_hunt_list, signal_file)
    with open("dodgelist.json", "w") as signal_file:
        json.dump(DodgeList, signal_file)
    add_Pokemon1.config(state="disabled")
    Continue.config(state="disabled")
    Stop.config(state="disabled")
    remove_Pokemon1.config(state="disabled")
    startProgram.destroy()
    program_thread = threading.Thread(target=run_program)
    program_thread.start()
def run_program():
    add_Pokemon1.config(state=tk.NORMAL)
    Stop.config(state=tk.NORMAL)
    Continue.config(state=tk.NORMAL)
    remove_Pokemon1.config(state=tk.NORMAL)
def stop_program():
    with open("stop.txt", "w") as signal_file:
        signal_file.write("pressed")
def add_pokemon():
    pokemon_name = entry_var.get()
    if pokemon_name in pokemon_list and pokemon_name not in pokemon_hunt_list and pokemon_name not in DodgeList:
        pokemon_hunt_list.append(pokemon_name)
        update_pokemon_list()
    entry_var.set("")

def continue_program():
    with open("signal.txt", "w") as signal_file:
        signal_file.write("pressed")
    with open("stop.txt", "w") as signal_file:
        signal_file.write("")
    with open("pokemon_List.json", "w") as signal_file:
        json.dump(pokemon_hunt_list, signal_file)
    Continue.config(state="disabled")
    Stop.config(state="disabled")
    add_Pokemon1.config(state="disabled")
    remove_Pokemon1.config(state="disabled")
    program_thread = threading.Thread(target=run_program)
    program_thread.start()
    
def add_pokemon2():
    pokemon_name = content
    if pokemon_name not in pokemonidentifiedList:
        with open("pokemonfound.txt","a") as file:
            file.write(pokemon_name+',')
        pokemonidentifiedList.append(pokemon_name)
    update_pokemon_list2()
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
    for pokemon in pokemonidentifiedList:
        text_widget2.insert(tk.END, f"{pokemon}\n")     
    text_widget["state"] = tk.DISABLED
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
        combo1.lift()  # Show the dropdown list4d

def on_select_combobox2(event=None):
    # Update the entry with the selected value from the combobox
    entry_var2.set(combo2.get())

    # Get the current value in the entry
    value2 = entry_var2.get().lower()

    # Find matches from the predefined list (pokemon_list)
    matches2 = [item for item in pokemonidentifiedList if item.lower().startswith(value2)]

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

def switch():
    global is_on
    # Determine is on or off
    if is_on:
        on_button.config(text = "up and down")
        with open("start.txt", "w") as start_file:
            start_file.write("s")
            is_on= False
    else:
        on_button.config(text = "left and right")
        with open("start.txt", "w") as start_file:
            start_file.write("a")
            is_on= True

def check_for_word(file_path, target_word):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return target_word in content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False
def update_label():
    global content
    if os.path.exists("pokemon.txt"):
        with open("pokemon.txt", 'r') as file:
            content = file.read()
        label1.config(text=f"PokemonFound: {content}")
        add_pokemon2()
    root.after(2000, update_label)
def main(): 
    global entry,entry2,tab1, tabControl,pokemon_hunt_list,text_widget,entry_var,combo,addpokemon1,DodgeList,entry_var1,combo1,root,is_on,pokemonidentifiedList
    global entry_var2,combo2,text_widget2,entry_var3,combo3,tab2,startProgram,add_Pokemon1,remove_Pokemon1,add_Pokemon2,remove_Pokemon2,on_button,root,label1
    pokemon_hunt_list = []
    DodgeList=[]
    is_on= True
    print(pokemonidentifiedList)
    if os.path.exists("pokemonfound.txt"):
        with open("pokemonfound.txt","r") as file:
            content=file.read()
            pokemonidentifiedList = [name.strip() for name in content.split(',')]
            pokemonidentifiedList.pop()
    with open("start.txt", "w") as start_file:
            start_file.write("a")
    addpokemon1=""
    root = tk.Tk() 
    root.title("Tab Widget") 
    root.geometry("500x500")
    tabControl = ttk.Notebook(root)
    tab1 = ttk.Frame(tabControl) 
    tab2 = ttk.Frame(tabControl) 
  
    tabControl.add(tab2, text ='land hunting') 
    tabControl.pack(expand = 1, fill ="both") 
    
    label1 = ttk.Label(tab2, text="PokemonFound:")
    label1.grid(row=4, column=3, pady=10, padx=10, sticky=tk.NW)
    label3 = ttk.Label(tab2, text="pokemonHuntList:")
    label3.grid(row=0, column=0, pady=10, padx=10, sticky=tk.NW)
    ##pokemon hunting
    label3 = ttk.Label(tab2, text="pokemonHuntList:")
    label3.grid(row=0, column=0, pady=10, padx=10, sticky=tk.NW)

    text_widget = tk.Text(tab2, height=5, width=20, state=tk.DISABLED)
    text_widget.grid(row=1, column=0, pady=10, padx=10, sticky=tk.W)

    label4 = ttk.Label(tab2, text="pokemonPotentialList:")
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
    
    startProgram = ttk.Button(tab2, text="start Program", command=start_program)
    startProgram.grid(row=10, column=0, columnspan=5, pady=100, padx=10, sticky=tk.S)
    
    on_button = ttk.Button(tab2, text="left and right",
                   command = switch)
    on_button.grid(row=10,pady=100)
    entry_var2 = tk.StringVar()
    combo2 = ttk.Combobox(tab2, textvariable=entry_var2, postcommand=on_select_combobox2)
    combo2.grid(row=4, column=3, pady=10)
    combo2["values"] = pokemonidentifiedList
    combo2.bind("<<ComboboxSelected>>", on_select_combobox2)
    root.after(2000, update_label)
    root.mainloop()

if __name__ == "__main__":
    main()