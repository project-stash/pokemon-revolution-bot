# when the health goes down to very low, it will crash
import pyautogui as pg, sys,time,random
import pytesseract
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
        temp = 0
        driver.save_screenshot('my_image.png')
        im = Image.open('my_image.png')
        im = im.crop((1100,380,1200,401))
        file = 'my_file.png'
        im.save(file)
        hp= pytesseract.image_to_string(file,config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789%')[:-2]
        print(hp)
        try:
            temp = int(hp)
        except:
            hp = ''
        if hp == '':
            break
        time.sleep(0.5)
        actions = ActionChains(driver)
        actions.send_keys('1')
        actions.perform()
        time.sleep(0.5)
        actions.send_keys('2')
        actions.perform()
        time.sleep(1)
    
    
def hunt_land(mode,pokemonList,driver):
    DodgeList = ["Cryogonal"]
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
            elif name[0] in pokemonList:
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
    
def setupwebsite(driver):
    url = "https://pokemon-planet.com"
    driver.get(url)
    button = driver.find_element(By.ID, "playnow2")
    button.click()
    button = driver.find_element(By.ID, "user")
    button.send_keys("invincibletroll")
    button = driver.find_element(By.ID, "passwrd")
    button.send_keys("chi020725")
    button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    button.click()
    button = driver.find_element(By.ID, "playnowbutton")
    button.click()
    
def main():
    driver = setupInfo()
    setupwebsite(driver)
    pokemonList=['Abra',
                 'Sneasel', 'Snorunt', 'Snover', 'Spheal', 'Swinub' ,
                 'Articuno']
    print("press when start program")
    y = input()
    mode = 'a'
    driver.set_window_size(1722, 1034)
    actions = ActionChains(driver)
    actions.key_down('b')
    actions.key_up('b')
    actions.perform()
    while True:
        hunt_land(mode,pokemonList,driver)
        print("decision: c for continue")
        x=input()
        if x != 'c':
            break
    

if __name__ == "__main__":
    main()