import sys,time
import winsound
import pytesseract
import os
import PySimpleGUI as sg
import pyautogui
import cv2
import pygetwindow
from PIL import Image
from pokemonlist import pokemon_list
from difflib import get_close_matches
import json
import random
#from plyer import notification
def walk(mode):
    if mode == 'a':
        pyautogui.keyDown("a")
        time.sleep(random.randint(0,5)/10)
        pyautogui.keyUp('a')
        return 'd'
    elif mode == 's':
        pyautogui.keyDown("s")
        time.sleep(random.randint(0,5)/10)
        pyautogui.keyUp('s')
        return 'w'
    elif mode == 'd':
        pyautogui.keyDown("d")
        time.sleep(random.randint(0,5)/10)
        pyautogui.keyUp('d')
        return 'a'
    else:
        pyautogui.keyDown("w")
        time.sleep(random.randint(0,5)/10)
        pyautogui.keyUp('w')
        return 's'

def check_for_word(file_path, target_word):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return target_word in content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False    
    
def hunt_land(mode,pokemonList):
    while True:
        mode = walk(mode)
        name = checkEncounter()
        print(name)
        if name in pokemon_list:
            with open("pokemon.txt", "w") as signal_file:
                signal_file.write(name)
        else:
            with open("pokemon.txt", "w") as signal_file:
                signal_file.write("")
        if name != None:
            Bl = check_special(name)
            if Bl == 'Special':
                winsound.Beep(440, 1000)
                sg.Popup(f"rare pokemon encounter")
                break
            elif name in pokemonList:
                winsound.Beep(440, 1000)
                sg.Popup(f"{name} pokemon encounter")
                break
            elif check_for_word("stop.txt", "pressed"):
                break
            else:
                pyautogui.press("4")
            window = pygetwindow.getWindowsWithTitle('PROClient')[0]
            left,top = window.topleft
            right,bottom = window.bottomright
            window.activate()
def check_special(name):
    return 'Normal'

def dissect_string(input_string):
    # Find the index of the first space
    space_index = input_string.find(' ')

    # Find the index of the first newline character after the space
    newline_index = input_string.find('\n', space_index)

    # Extract the substring between the space and newline
    if newline_index != -1:  # If newline found
        extracted_string = input_string[space_index + 1:newline_index]
    else:
        extracted_string = input_string[space_index + 1:]

    return extracted_string    
def checkEncounter():
    titles = pygetwindow.getAllTitles()
    window = pygetwindow.getWindowsWithTitle('PROClient')[0]
    left,top = window.topleft
    right,bottom = window.bottomright
    window.activate()
    path = 'result.png'
    pyautogui.screenshot(path)
    im = Image.open(path)
    #im=im.crop((left+450,top+140,right-10,bottom-650))
    im=im.crop((left+450,top+130,right-10,bottom-650))
    file= 'result.png'
    im.save(file)
    #extracted_text= pytesseract.image_to_string(file,config="--psm 10")
    extracted_text= pytesseract.image_to_string(file)
    result = dissect_string(extracted_text)
    words= result.split()
    if len(words) > 0:
        if words[0] == "Wild":
            result = words[1]
        else:
            pass
    return result

    
def main():
    x = False
    pokemonList=[]
    signal_file = "signal.txt"
    while not os.path.exists(signal_file):
        time.sleep(1)

    # Remove the signal file
    os.remove(signal_file)
    if check_for_word("start.txt", "a"):
            mode = 'a'
    else:
            mode = 's'
    signal_file = "pokemon_List.json"
    while not os.path.exists(signal_file):
        time.sleep(1)
    with open(signal_file, 'r') as file:
        pokemonList=json.load(file)
    os.remove(signal_file)
    titles = pygetwindow.getAllTitles()
    window = pygetwindow.getWindowsWithTitle('PROClient')[0]
    left,top = window.topleft
    right,bottom = window.bottomright
    window.activate()
    pyautogui.press('1')
    while True:
        print("yes")
        titles = pygetwindow.getAllTitles()
        window = pygetwindow.getWindowsWithTitle('PROClient')[0]
        left,top = window.topleft
        right,bottom = window.bottomright
        window.activate()
        hunt_land(mode, pokemonList)
        
        # Wait for the signal to continue
        signal_file_path = "signal.txt"
        while not os.path.exists(signal_file_path):
            time.sleep(1)
        # Check for the stop signal
        if check_for_word("stop.txt", "pressed"):
            x = True
        # Remove the signal file
        os.remove(signal_file_path)
        # Exit the loop if stop signal received
        if x:
            print("break")
            break

        # Update pokemonList from file
        pokemon_list_file_path = "pokemon_List.json"
        while not os.path.exists(pokemon_list_file_path):
            time.sleep(1)
            print("Waiting for pokemon_List.json...")
        with open(pokemon_list_file_path, 'r') as file:
            pokemonList = json.load(file)
        os.remove(pokemon_list_file_path)

        # Update DodgeList from file
        dodge_list_file_path = "dodgelist.json"
        if check_for_word("start.txt", "a"):
            mode = 'a'
        else:
            mode = 's'
        
    

if __name__ == "__main__":
    # Call the main function
    main()