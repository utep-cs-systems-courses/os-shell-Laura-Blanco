import re,os
from os import read

Index = 0
buf = 0

def getChar():
    global Index,buf

    if Index == buf:
        Index = 0
        buf = read(0,1000) #fills array with input from keyboard
        if buf == 0: #if there is nothing then end of file has been reached
            return None
    if Index < len(buf) -1: #checks to make sure the index is still in bounds
        newBuf = buf.decode() #decode returns string 
        character = newBuf[Index] #gets the character from current index
        Index += 1 
        return character
    return None  #index out of bounds

def readLine():
    global Index,buf
    line = ""
    character = getChar()
    
    while character != '\n' and character != None: #as long as character is valid build the line
        line += character
        character = getChar()  #get next character
    Index = 0
    buf = 0
   # os.write(1,f"{str(line)} \n".encode())
    return line
#readLine()
