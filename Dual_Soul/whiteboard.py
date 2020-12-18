from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key
import time
specialkey_dic = {"Key.enter":Key.enter}
kb = keyboard.Controller()

time.sleep(2)

kb.press(specialkey_dic["Key.enter"])
kb.release(specialkey_dic["Key.enter"])
#kb.press(Key.enter)
