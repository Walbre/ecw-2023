import socket,os, time

os.chdir(os.path.dirname(__file__))


con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.setdefaulttimeout(10)

addr, port = "instances.challenge-ecw.fr", 41115

con.connect((addr, port))

print(con.recv(1024).decode())

print(con.recv(1024).decode())

rep1 = "yes"
con.send(rep1.encode())

print(f"{rep1}\n")

print(con.recv(1024).decode())

rep2 = "42"
con.send(rep2.encode())

print(f"{rep2}\n")

prev = con.recv(1024).decode()

print(prev)

### Question 3.

def q3(prev):

    prev = prev.split(":")

    nb = ord(prev[1].replace(" ", "").replace("\n", "")) - 97
    coeff = 1 if "after" in prev[0] else (-1)
    nb = (nb + coeff) % 26
    nb += 97

    rep3 = chr(nb)
    return rep3

rep3 = q3(prev)

con.send(rep3.encode())

print(f"{rep3}\n")

prev = con.recv(1024).decode()

### Q4

print(prev)

def q4(prev):
    colors = ["red", "green", "blue"]

    prev = prev.split(":")[1].replace(" ", "").replace("\n", "").split(",")

    if prev == ["0", "0", "0"]:
        rep4 = "black"
    elif prev == ["255", "255", "255"]:
        rep4 = "white"
    else:
        rep4 = colors[prev.index("255")]
    
    return rep4

rep4 = q4(prev)

print(f"{rep4}\n")

con.send(rep4.encode())

prev = con.recv(1024).decode()

### Q5

print(prev)

prev = con.recv(1024).decode()

print(prev)

rep5 = f"{rep1},{rep2},{rep3},{rep4}"

print(rep5)

con.send(rep5.encode())

prev = con.recv(1024).decode()

print(prev)

### Q6

def q6(prev):
    question = prev[prev.index("question(s)") + 11:prev.index("using")].replace(" ", "")


    rep_list = []

    for n in question.split(","):
        rep_list.append(eval(f"rep{n}"))

    rep6 = ",".join(rep_list)
    return rep6

rep6 = q6(prev)

print(rep6)

con.send(rep6.encode())

prev = con.recv(1024).decode()

print(prev)

### Q7

def q7(prev:str):
    
    question = prev[prev.index(":") + 2:]
    
    corresp = {
        "Do you wanna play a game?" : lambda x:"yes",
        "What is the meaning of life, the universe, and everything, according to Deep Thought?": lambda x:"42",
        "Easy question, Which letter comes" : q3,
        "Can you tell me what color is :" : q4,
        "I forgot everything. Send me back your answers to questions 1 to 4, separated by commas.": lambda x: rep1+","+rep2+","+rep3+","+rep4,
        "I did not understand. Can you repeat your previous answers for question(s)" : q6,
    }
    
    for cond, action in corresp.items():
        if question.replace(" ", "").lower().startswith(cond.replace(" ", "").lower()):
            return action(question)

rep7 = q7(prev)

print(rep7)

con.send(rep7.encode())

prev = con.recv(1024).decode()

print(prev)

prev = con.recv(1024).decode()

print(prev)


### Q8


def decode_braille(line):
    ascii_verion = "abcdefghijklmnopqrstuvwxyz?!1234567890"
    braille_version = "⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚⠅⠇⠍⠝⠕⠏⠟⠗⠎⠞⠥⠧⠺⠭⠽⠵⠦⠖⠁⠆⠉⠙⠢⠋⠛⠓⠊⠚"
    assert len(ascii_verion) == len(braille_version)
    
    newline = ""
    for letter in line:
        if letter in braille_version:
            newline += ascii_verion[braille_version.index(letter)]
        else:
            newline += letter
    
    return newline

def decode_morse(line:str):
    ascii_version = "abcdefghijklmnopqrstuvwxyz?!:.,ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    morse_version = ".-/-.../-.-./-.././..-./--./..../../.---/-.-/.-../--/-./---/.--./--.-/.-./.../-/..-/...-/.--/-..-/-.--/--../..--../-.-.--/---.../.-.-.-/--..--/.-/-.../-.-./-.././..-./--./..../../.---/-.-/.-../--/-./---/.--./--.-/.-./.../-/..-/...-/.--/-..-/-.--/--../-----/.----/..---/...--/....-/...../-..../--.../---../----.".split("/")
    
    decomposed_line = line.replace('\n', '').split(" ")
    
    newline = ""
    for letter in decomposed_line:
        if letter in morse_version:
            newline += ascii_version[morse_version.index(letter)]
        elif letter == "/":
            newline += " "
        elif letter in "012345678.9":
            newline += letter
        elif letter != " ":
            newline += f"ATTENTION>{letter}<ATTENTION"
    
    return newline
    
def q8(prev):
    if "/" in prev:
        rep8 = decode_morse(prev)
    else:
        rep8 = decode_braille(prev)
        rep8 = rep8.replace(" ", "").replace("⠀", " ")
    
    return rep8.split(":")[1][1:]

rep8 = q8(prev)

print(rep8)

con.send(rep8.encode())

prev = con.recv(1024)

print(prev)

### Q9

with open('test.png', 'wb') as f:
    f.write(prev[3:])

from pyzbar.pyzbar import decode
from PIL import Image

def q9():
    decocdeQR = decode(Image.open('test.png'))
    rep9 = decocdeQR[0].data.decode('ascii')
    return rep9

rep9 = q9()

rep9 = rep9.split(":")[1][1:].replace("\n", "")

print(rep9)

con.send(rep9.encode())

prev = con.recv(2048)

print(prev)

### Q10



with open('test.png', 'wb') as f:
    f.write(prev[4:])
    
    
def q10():
    decocdeQR = decode(Image.open('test.png'))
    rep10 = decocdeQR[0].data.decode('utf-8')
    print(rep10)
    if "/" in rep10:
        rep10 =  decode_morse(rep10)
    else:
        rep10 = decode_braille(rep10).replace(" ", "").replace("⠀", " ")
    print(rep10)
    rep10 = q7(rep10)
    print(rep10)
    return rep10

rep10 = q10()

con.send(rep10.encode())

prev = con.recv(1024).decode()

print(prev)

print(con.recv(1024).decode())