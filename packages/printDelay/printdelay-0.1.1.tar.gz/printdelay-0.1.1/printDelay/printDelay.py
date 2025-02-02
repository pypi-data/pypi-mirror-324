import time
import sys

#prints without a newline
def printf (string,sec):
    for x in string:
        print(x,end='')
        time.sleep(sec)
    
#prints with a newline
def printl (string,sec):
    print()
    for x in string:
        print(x,end='')
        time.sleep(sec)
    
