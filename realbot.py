import pygetwindow
import pyautogui
from PIL import Image
import time
import pytesseract
#from AppOpener import open
#open("PROClient")
path = 'result.png'
titles = pygetwindow.getAllTitles()
window = pygetwindow.getWindowsWithTitle('PROClient')[0]
left,top = window.topleft
right,bottom = window.bottomright
window.activate()
time.sleep(1)
pyautogui.screenshot(path)
im = Image.open(path)
im=im.crop((left+450,top+130,right-10,bottom-650))
im.show(path)
file= 'result.png'
im.save(file)

extracted_text= pytesseract.image_to_string(file)
#print(extracted_text+"1")
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
result = dissect_string(extracted_text)
print(result)