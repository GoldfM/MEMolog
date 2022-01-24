import socket, time
from PIL import Image, ImageTk
from tkinter import Tk, Label, Button
from threading import Thread
window = Tk()
window["bg"] = "#362b2b"
window.geometry("1400x830")
window.title("NEO. Math helper")
window.resizable(False, False)

host = socket.gethostbyname(socket.gethostname())
server = ("26.185.136.111", 12345)
port = 0 # socket server port number
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # instantiate
sock.bind((host,port))
sock.connect(server) # connect to the server

sock.sendto(input().encode('utf-8'),server)
PLAYER=2
def choiser():
    data, addr = sock.recvfrom(2048)
    data=data.decode('utf-8').split(';')
    situation=data[0]
    with open(r'game_text.txt',encoding='utf-8') as f:
        situation=str(f.read()).split(';')[int(situation)]
    nums=data[1:7]
    list_btns=[]
    head=Label(text=situation,font="Calibri 23 bold",justify="center",bg="#362b2b",fg="#f67300")
    head.place(x=120,y=20)
    dict_pict_btn={nums[0]:0,nums[1]:1,nums[2]:2,nums[3]:3,nums[4]:4,nums[5]:5}
    x=200
    y=120
    i=0


    for num in nums:
        print(i)
        com = lambda x=num: send_num_picture(x)
        btn = Button(window,command=com)
        img = Image.open(f"mems\\{num}.jpg").resize((300,300))
        btn.img = ImageTk.PhotoImage(img)
        btn['image'] = btn.img
        btn.place(x=x,y=y,width=310,height=310)
        x+=350
        i+=1
        if x>1000:
            y=480
            x=200
        list_btns.append(btn)
    print(list_btns)
    def send_num_picture(i):

        print('HII  1')
        sock.sendto(f'{i}'.encode('utf-8'), server)
        print('HII  2')
        end_round()
    def end_round():
        print('HII  3')
        for btn in list_btns:
            btn.destroy()

        data, addr = sock.recvfrom(2048)
        print('HII  4')
        data = data.decode('utf-8')
        print(data)
        datas = data.split(';')[0:-1]
        for data in datas:
            data=data.split('|')
            lbl_name=Label(text=(' '+data[0]),font="Calibri 25 bold",justify="center",bg="#362b2b",fg="#f67300")
            lbl_name.place(x=100,y=370)
            pict = Label(window)
            img = Image.open(f"mems\\{data[1]}.jpg").resize((640, 640))
            pict.img = ImageTk.PhotoImage(img)
            pict['image'] = pict.img
            pict.place(x=450, y=130, width=650, height=650)
            window.update()
            print('Я заплейсил картинку')
            time.sleep(4)
            lbl_name.destroy()
            pict.destroy()
        head.destroy()
        choiser()




recvThread = Thread(target=choiser)
recvThread.daemon = True
recvThread.start()
window.mainloop()



