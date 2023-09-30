#Test for python CS:Inv
import requests
import json
import time
from nicegui import ui

#file = '.\CS_INV_DATA.json'
file = '.\source\CS_INV_DATA.json'

test = {'name' :'Gamma Case', 'amount' : 31, 'value' : 0 ,  'url' : 'http://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name=Gamma%20Case'}



try:
    with open(file, 'r') as openfile:
        inv = json.load(openfile) 
except:
    print('cant read data')

def total():
    sum = 0
    for x in inv:
        sum = sum + (x['amount'] * x['value'])  
    print(f'Total value: ${sum}')
    return sum


def update():
    for item in inv:
        for attempt in range(10):
            try:
                req = requests.get(item['url'])
                data = json.loads(req.text)
                if(req.status_code != 200):
                    raise Exception("error")
                item.update({'value' : float(data['lowest_price'].split('$')[1])})
            except:
                print(f'attempt: {attempt} status: {req.status_code}')
                time.sleep(4)
                continue
            else:
                break
        print(f"{item['name']}: ${item['amount']*item['value']}")

    try:
        with open(file , 'w') as outfile:
            json.dump(inv, outfile, indent=4)
            print('wrote successfully')
    except:
        print('writing aborted')
    totalValue = total
    




while True:
    print('update/totalValue')
    userInput = input()
    #in = input.lower()
    if(userInput == 'update'):
        update()
    elif(userInput == 'totalValue'):
        total()
    else:
        continue

"""
totalValue = total()

dark = ui.dark_mode()
dark.enable()

columns = [
    {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left', 'sortable': True},
    {'name': 'amount', 'label': 'Amount', 'field': 'amount', 'sortable': True},
    {'name': 'value', 'label': 'Value', 'field': 'value', 'sortable': True},

]
rows = []

for item in inv:
    rows.append({'name': item['name'], 'amount': item['amount'], 'value': item['value'],})

ui.table(columns=columns, rows=rows, row_key='name')

ui.button('Update', on_click=update()).

ui.label(f'Total Value: $ {totalValue}')
ui.run()

"""