########################################
#import

from textwrap import shorten
import requests
import json
import time
import math
from prettytable import PrettyTable

########################################
#cost

source = '.\CS_INV_DATA.json'
source2 = '.\source\CS_INV_DATA.json'
file = ''

########################################
#def

def openFile():
    global file
    try:
        
        with open(source, 'r') as openfile:
            inv = json.load(openfile)
        file = source
    except:
        try:
            
            with open(source2, 'r') as openfile:
                inv = json.load(openfile)
            file = source2
        except:
            print('cant read data')
    finally:
        return inv

def update(delay):
    print(f'Estimated Time: {round((len(inv)/20),2)} min')
    for item in inv:
        for attempt in range(10):
            try:
                req = requests.get(item['url'])
                data = json.loads(req.text)
                if(req.status_code != 200):
                    raise Exception("error")
                item.update({'value' : float(data['lowest_price'].split('$')[1])})
                time.sleep(1*delay)
            except:
                print(f'attempt: {attempt} status: {req.status_code}')
                time.sleep(4*delay)
                continue
            else:
                break
        print(f"{item['name']}: ${item['value']}")

    try:
        with open(file, 'w') as outfile:
            json.dump(inv, outfile, indent=4)
            print('wrote successfully')
    except:
        print('writing aborted')

def show():
    table = PrettyTable(['Name', 'Amount', 'Value', 'Total Value'])
    for item in inv:
       table.add_row([item['name'], item['amount'], '$'+str(round(item['value'], 2)), '$'+str(round(item['value']*item['amount'], 2))])
    t_val = 0
    t_amo = 0
    for x in inv:
        t_val = t_val + (x['amount'] * x['value'])
        t_amo = t_amo + x['amount']
    
    table.add_row(['', '', '', ''])
    table.add_row(['Total:', t_amo, '', '$'+str(round(t_val, 2))])
    print(table)
    print('\n')

########################################
#Main

#init
inv = openFile()

#mainloop
while True:
    print('update/show')
    userInput = input()
    userInput = userInput.lower()
    if(userInput == 'update'):
        update(3)
    elif(userInput == 'show'):
        show()
    else:
        continue

########################################