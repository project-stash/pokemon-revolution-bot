import sys,time
import pytesseract
import os
import PySimpleGUI as sg
import cv2
from selenium import webdriver
from PIL import Image
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pokemonlist import pokemon_list
import json
#from plyer import notification
def walk(mode,driver):
    if mode == 'a':
        actions = ActionChains(driver)
        actions.key_down("a")
        actions.perform()
        time.sleep(0.5)
        actions.key_up("a")
        actions.perform()
        return 'd'
    elif mode == 's':
        actions = ActionChains(driver)
        actions.key_down("s")
        actions.perform()
        time.sleep(0.5)
        actions.key_up("s")
        actions.perform()
        return 'w'
    elif mode == 'd':
        actions = ActionChains(driver)
        actions.key_down("d")
        actions.perform()
        time.sleep(0.5)
        actions.key_up("d")
        actions.perform()
        return 'a'
    else:
        actions = ActionChains(driver)
        actions.key_down("w")
        actions.perform()
        time.sleep(0.5)
        actions.key_up("w")
        actions.perform()
        return 's'
def kill(driver):
    while True:
        name = checkEncounter(driver)
        #print(name)
        B1 = ''
        if name[0] != None:
            B1 = check_special(name)
        if B1 == 'Normal' and name[0] not in pokemon_list and '-Christmas' not in name[0]:
            break
        elif B1 == '':
            break
        while True:
            driver.save_screenshot('my_image.png')
            im = Image.open('my_image.png')
            im = im.crop((1000,800,1100,850))
            file= 'my_file.png'
            im.save(file)
            img = cv2.imread("my_file.png")
            gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gry, (3,3), 0)
            thr = cv2.threshold(blur, thresh=0, maxval=255, type=cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
            hp= pytesseract.image_to_string(thr,config="--psm 10")
            #print(hp)
            if hp == 'Fight:\n':
                actions = ActionChains(driver)
                actions.send_keys('1')
                actions.perform()
                time.sleep(0.5)
                actions.send_keys('2')
                actions.perform()
            break
        time.sleep(1)
    
    
def hunt_land(mode,pokemonList,driver,DodgeList):
    while True:
        mode = walk(mode,driver)
        name = checkEncounter(driver)
        if name[0] != None:
            Bl = check_special(name)
            if Bl == 'Shiny':
                name = name[1][3:]
                sg.Popup(f"pokemon Appeared, it's a shiny {name}")
                break
            elif Bl == 'Elite':
                name = name[1][3:]
                sg.Popup(f"pokemon Appeared, it's a Elite {name}")
                break
            elif name[0] in pokemonList or ('-Christmas' in name[0] and name[0][:-10] in pokemonList):
                sg.Popup(f"pokemon Appeared, it's a {name[0]}")
                break
            elif name[0] in DodgeList:
                actions = ActionChains(driver)
                actions.send_keys('4')
                actions.perform()
            elif name[0] in pokemon_list or '-Christmas' in name[0]:
                kill(driver)
def check_special(name):
    if name[1].startswith('[S]') or name[1].startswith('{S]'):
        return 'Shiny'
    elif name[1].startswith('[E]') or name[1].startswith('{E]'):
        return 'Elite'
    else:
        return 'Normal'
    
def checkEncounter(driver):
    driver.save_screenshot('my_image.png')
    image = 'my_image.png'
    new_image = 'savedImage.png'
    im = Image.open(image)
    im = im.crop((950,332,1200,375))
    file= 'my_file.png'
    im.save(file)
    out = cv2.imread('my_file.png')
    gray = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cv2.imwrite(new_image,thresh)
    extracted_text= pytesseract.image_to_string(thresh,config="--psm 10")
    extracted_text2= pytesseract.image_to_string(file,config="--psm 10")
    if extracted_text == '':
        return (None, None)
    else:
        return (extracted_text[:-1],extracted_text2[:-1])
def setupInfo():
    edge_options = Options()
    edge_options.add_experimental_option("detach", True)
    #edge_options.add_argument('headless')
    service = Service(executable_path='./msedgedriver.exe')
    driver = webdriver.Edge(service = service,options = edge_options)
    return driver
    
def setupwebsite(driver,username,password):
    url = "https://pokemon-planet.com"
    driver.get(url)
    button = driver.find_element(By.ID, "playnow2")
    button.click()
    button = driver.find_element(By.ID, "user")
    button.send_keys(username)
    button = driver.find_element(By.ID, "passwrd")
    button.send_keys(password)
    button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    button.click()
    button = driver.find_element(By.ID, "playnowbutton")
    button.click()
def check_for_word(file_path, target_word):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return target_word in content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False
    
def main(username, password):
    x = False
    driver = setupInfo()
    driver.set_window_size(1722, 1034)
    print(driver.get_window_size())
    setupwebsite(driver,username,password)
    pokemonList=[]
    DodgeList = []
    signal_file = "signal.txt"
    while not os.path.exists(signal_file):
        time.sleep(1)

    # Remove the signal file
    os.remove(signal_file)
    mode = 'a'
    signal_file = "pokemon_List.json"
    while not os.path.exists(signal_file):
        time.sleep(1)
    with open(signal_file, 'r') as file:
        pokemonList=json.load(file)
    os.remove(signal_file)
    signal_file = "dodgelist.json"
    while not os.path.exists(signal_file):
        time.sleep(1)
    with open(signal_file, 'r') as file:
        DodgeList=json.load(file)
    os.remove(signal_file)
    actions = ActionChains(driver)
    actions.key_down('b')
    actions.key_up('b')
    actions.perform()
    while True:
        hunt_land(mode,pokemonList,driver,DodgeList)
        with open("return.txt", "w") as signal_file:
             signal_file.write("pressed")
        signal_file = "signal.txt"
        while not os.path.exists(signal_file):
            time.sleep(1)
        if check_for_word("stop.txt", "pressed"):
            x = True
        os.remove(signal_file)
        if x == True:
            break
        # signal_file = "pokemon_List.json"
        # while not os.path.exists(signal_file):
        #     time.sleep(1)
        # with open(signal_file, 'r') as file:
        #     pokemonList=json.load(file)
        # os.remove(signal_file)
        # signal_file = "dodgelist.json"
        # while not os.path.exists(signal_file):
        #     time.sleep(1)
        # with open(signal_file, 'r') as file:
        #     DodgeList=json.load(file)
        # os.remove(signal_file)
        
    

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python pokemon.py <username> <password>")
        sys.exit(1)

    # Get username and password from command-line arguments
    username = sys.argv[1]
    password = sys.argv[2]

    # Call the main function with username and password
    main(username, password)