import pygetwindow
import pyautogui
from PIL import Image
import time
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
window_left, window_top, window_width, window_height = window.left, window.top, window.width, window.height
im=im.crop((left+630,top+ 700,right-10,bottom-10))
pyautogui.click(x=left+630, y=top+ 700)
pyautogui.click(x=left+630, y=top+ 710)
time.sleep(5)
pyautogui.press('1')
#im.show(path)