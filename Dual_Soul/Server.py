import socket
import threading
import sys
import time
from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key



class server():
    def __init__(self):
        #Misc Parameters
        self.format = "utf-8"
        self.header = 128
        self.port = 5050
        self.disconnect_msg = "!!disconnect"
        self.specialkey_dic = {"Key.enter":Key.enter}

        #Setting up and initiating the Server
        self.server_ip = "127.0.0.1" #socket.gethostbyname(socket.gethostname())
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.addr = (self.server_ip,self.port)
        print(self.server_ip)
        print(self.server)
        print(self.addr)

        #Initiating Both Controllers
        self.mousecontroller  = mouse.Controller()
        self.keyboardcontroller  = keyboard.Controller()


        self.already_set_up = False

    def mouse_input(self,code,data):
        
        #Mimic Mouse input making Function
        if code == "PC":
            #In case of a [P]ostion [C]hange of the mouse
            self.mousecontroller.position = (int(data[0]),int(data[1]))
        elif code == "P":
            ### In case of a Mouse button pressed
            if data[2] == "Button.left":
                #Press left
                self.mousecontroller.press(Button.left)
            else:
                #Or rigth
                self.mousecontroller.press(Button.right)
        elif code == "R":
            if data[2] == "Button.left":
                #Release left
                self.mousecontroller.release(Button.left)
            else:
                #Or rigth
                self.mousecontroller.release(Button.right)
        #Scroll handlers
        elif code == "SU":
            #Scroll up 
            self.mousecontroller.scroll(0,1)
        elif code == "SD":
            #Scroll Down
            self.mousecontroller.scroll(0,-1)

    def keyboard_input(self,code,data):
        print("code :",code," data :",data)
        ### Mimic Keyboard input making Function
        try:
            #Press the key
            if code == "P":
                if data in self.specialkey_dic.keys():
                    print("datum :", str(data[0]))
                    self.keyboardcontroller.press(self.specialkey_dic[str(data[0])])
                else:
                    self.keyboardcontroller.press(str(data[0]))
            #Release it
            elif code == "R":
                if data in self.specialkey_dic.keys():
                    self.keyboardcontroller.release(self.specialkey_dic[str(data[0])])
                else:
                    self.keyboardcontroller.release(str(data[0]))
        except Exception as e :
            print(e)


    def adaptative_input(self,input_type,code,data):
        ### Redirect the message to the correct Inputmaking function 
        try:
            if input_type == "MG":#"M" is the original signal , Changed it to MG otherwise on solo computer test your mouse is fucked
                self.mouse_input(code,data)

            elif input_type == "K":
                self.keyboard_input(code,data)

        except Exception as e:
            #print(e)
            pass

    def correct_data(self,data):
        return data.replace("'","")


    def handle_client(self,conn,addr):
        print("New Connection ",addr)
        self.connected = True

        while self.connected:
            msg_lenght = conn.recv(self.header).decode(self.format)
            if msg_lenght:
                try:
                    #try auto skip wrong packets ?
                    msg_lenght = int(msg_lenght)
                    msg= conn.recv(msg_lenght).decode(self.format)
                    if msg == "!!disconnect":
                        connected = False
                        return False
                    msg = tuple(msg.split(' '))
                    print(msg)
                    data = [self.correct_data(msg[2]),msg[3],msg[4] if msg[4] else None]
                    self.adaptative_input(msg[0],msg[1],data)
                    #print(addr,"said : ",msg)
                    #conn.send(str(msg).encode(self.format))
                except Exception as e:
                    #print("Skipped packet",e)
                    pass

        conn.close()
        sys.exit()

    def start(self):
        #Start the server Listening Process put every Connection into a new thread 
        print("[STARTING]...")

        self.server.bind(self.addr)
        self.server.listen()
        print("[Listenning] Server listenning : on ",self.addr)
        while True:
            conn,addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client,args=(conn, addr))
            thread.daemon = True
            thread.start()
        #print("Current Connection(s?) ",threading.activeCount() - 1)

    def stop(self):
        #stop the server and prepare it for a a new Start input
        self.connected = False
        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)



