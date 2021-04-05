import re
from time import sleep
import socket

HOST = "irc.twitch.tv"
PORT = 6667
NICK = ""
KEY = "oauth:"
CHANNEL = "#"
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")


def loop():
    try:
        s = socket.socket()
        s.connect((HOST, PORT))
        s.send("PASS {}\r\n".format(KEY).encode("utf-8"))
        s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
        s.send("JOIN {}\r\n".format(CHANNEL).encode("utf-8"))
        connect = True
    except Exception as e:
        print(str(e))
        connect = False

    while connect:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode())
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)

            if message.strip() == "!hello":
                privchat(s, username.strip(), "Hello World!")

            if message.strip() == "!hi":
                chat(s, "Hello World!")

            print(username + ": " + message)
        sleep(1)

def chat(sock, msg):
    sock.send("PRIVMSG #mrwejq :{}\r\n".format(msg).encode("utf-8"))

def privchat(sock, user, msg):
    msg = "@"+user+" "+msg
    sock.send("PRIVMSG #mrwejq :{}\r\n".format(msg).encode("utf-8"))

if __name__ == "__main__":
    loop()
