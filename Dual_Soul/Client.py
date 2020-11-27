import socket
import threading
from pynput import keyboard,mouse
import time
import sys
import Input_Modification as IM

class Client():
    def __init__(self):
# Misc Param
        self.format = "utf-8"
        self.header = 128
        self.port = 5050
        self.disconnect_msg = "!!disconnect"
        self.key_allower = keyboard.Key.ctrl

#Global States

        self.key_state = False
        self.locked_key_state = False

#Backend Prep

        self.client_ip = socket.gethostbyname(socket.gethostname())
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.addr = ("127.0.1.1",self.port)
        self.preferences = open("Preferences.txt")
        self.translation_table = IM.extract_Translation_Table(self.preferences.read())
        print(self.translation_table)


    def send(self,msg):
        message = msg.encode(self.format)
        msg_lenght = len(message)
        send_lenght = str(msg_lenght).encode(self.format)
        send_lenght += b' ' * (self.header - len(send_lenght))
        self.client.send(send_lenght)
        self.client.send(message)
        #print(self.client.recv(2048))

    def allower_checker(self,key):
        #Function used to swap state of the Allower
        global key_state
        if key == self.key_allower:
            self.key_state = not self.key_state
        return self.key_state

    def on_press_key(self,key):
        ### Will send a message only if the Allower state is true
        self.key_state = self.allower_checker(key)
        print(self.translation_table[str(key)])
        if self.key_state or self.locked_key_state:
            try:
                if key in self.translation_table:
                    self.send(str("{0} {1} {2} {3} {4}".format("K","P",self.translation_table[key],None,None)))
                else:
                    self.send(str("{0} {1} {2} {3} {4}".format("K","P",key,None,None)))
            except AttributeError:
                print('special key {0} pressed'.format(key))

    def on_release_key(self,key):
        #self.allower_checker(key)
        if self.key_state:
            try :
                if key in self.translation_table:
                    self.send(str("{0} {1} {2} {3} {4}".format("K","R",self.translation_table[key],None,None)))
                else:
                    self.send(str("{0} {1} {2} {3} {4}".format("K","R",key,None,None)))
                
                
                if key == keyboard.Key.esc:
                    #send("!!disconnect")
                    #return False
                    pass
            except AttributeError:
                print('special key {0} pressed'.format(key))

#mouse inner working
    def on_move_mouse(self,x, y):
        try:
            self.send("{0} {1} {2} {3} {4}".format("M","PC",x,y,None))
            return None
        except:
            pass

    def on_click_mouse(self,x, y, button, pressed):
        #print(pressed)
        self.send(str(('{0} {1} {2} {3} {4}'.format("M","P" if pressed else "R",x,y,button))))


    def on_scroll_mouse(self,x, y, dx, dy):
        self.send(str('M {0} {1} {2} {3} '.format("SD" if dy < 0 else 'SU',x,y,None)))


    def on_activate_lock(self):
        print('<ctrl>+<alt>+<space> pressed')
    
    def on_activate(self):
   
        global locked_key_state
        self.locked_key_state = not self.locked_key_state

    def for_canonical(self,f):
        return lambda k: f(self.l.canonical(k))

    def start(self):

        self.hotkey = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+<alt>+h'),self.on_activate)

        with keyboard.Listener(
            on_press=self.for_canonical(self.hotkey.press),
            on_release=self.for_canonical(self.hotkey.release)) as l:
            self.l = l

            self.client.connect(self.addr)

            self.listenerkeyboard = keyboard.Listener(on_press=self.on_press_key,on_release=self.on_release_key)
            self.listenermouse = mouse.Listener(on_move=self.on_move_mouse,on_click=self.on_click_mouse,on_scroll=self.on_scroll_mouse)




            self.listenerkeyboard.start()
            self.listenermouse.start()

            self.listenerkeyboard.join()
            self.listenermouse.join()

            self.l.join()

    def stop(self):
        self.connected = False
        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
