import socket
import time
import random

PLAYERS=2
host = socket.gethostbyname(socket.gethostname())
port = 12345
print(host)
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((host,port))
start = True
check='wait'
addresses=[]
nums=list(range(0,130))
range_situations=list(range(0,len(open('game_text.txt','r' ).read().split(';'))))
players={}
list_picture=''
while start:
    if check=='wait':
        data,addr=sock.recvfrom(2048)
        addresses.append(addr)
        players[addr]=data.decode('utf-8')
        if len(addresses)==PLAYERS:
            check='start'
    elif check=='start':
        print(players)
        situation=random.choice(range_situations)
        range_situations.remove(situation)
        for adr in addresses:
            msg=f'{situation}'
            for _ in range(6):
                num=random.choice(nums)
                print(num)
                nums.remove(num)
                msg+=';'+str(num)
            sock.sendto(msg.encode('utf-8'),adr)
        check='game'
    elif check == 'game':
        for _ in range(PLAYERS):
            data, addr = sock.recvfrom(2048)
            print(f'{players[addr]} send picture number {data.decode("utf-8")}')
            list_picture+=players[addr]+'|'+data.decode("utf-8")+';'
        check='end'
    elif check == 'end':
        for adr in addresses:
            print(f'Отправил {adr} сообщение {list_picture}')
            sock.sendto(list_picture.encode('utf-8'),adr)
        check='start'
        list_picture=''
