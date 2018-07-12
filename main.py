import requests
import json
import time


URL     = "https://api.telegram.org/bot612780025:AAF_p1_77l061SAHmGnFjErSw3gCVz3D_4c/"
OFFSET  = 0
LIMIT   = 0 

def bot_about():
    text = """
    <b>Приветствую!</b>
    Я Бот! 
    Умею выводить курс криптовалюты по команде.
    Используй:
    <b>/btc</b> - актуальный курс биткоина
    <b>/eth</b> — актуальный курс эфириума
    """
    return text


def bot_info():

    method = "getMe"
    response = requests.get(URL + method)
    decoded = response.json()
    return json.dumps(decoded, indent=4)

def fetch_crypto(type):

    url_crypto = "https://api.cryptonator.com/api/ticker/"
    res = requests.get(url_crypto + type)
    if res.status_code==200:
        return res.json()['ticker']['price']

def massage_combine(item,text):
    message_data = { 
    'chat_id': item['message']['chat']['id'],               # куда отправляем сообщение
    'text': text,                                         # само сообщение для отправки 
    #'reply_to_message_id': item['message']['message_id'],   # если параметр указан, то бот отправит сообщение в reply
    'parse_mode': 'HTML' 
    }
    return message_data

def upd_handling():

    method = "getUpdates"
    global OFFSET

    par = {'limit': LIMIT, 'offset': OFFSET, 'timeout':3}
    print(par)
    try:
        result = requests.get(URL + method, params=par)
    except:
        print('Error getting updates')
        return False

    if not result.status_code == 200: return False
    if not result.json()['ok']: return False

    udates = result.json()['result']

    for item in udates:
         
        OFFSET = item['update_id']+1
        
        if 'message' not in item or 'text' not in item['message']: 
            print('Unknown message')
            continue

        # сообщение из чата
        message_id  = item['message']['message_id']
        text        = item['message']['text']
        print(message_id, text)

        # сообщение в ответ
        if not text.find("/start")==-1:
            message_data = massage_combine(item,bot_about()) 
            
        elif not text.find("/btc")==-1: 
            message_data = massage_combine(item,fetch_crypto("btc-usd"))
        elif not text.find("/eth")==-1:
            message_data = massage_combine(item,fetch_crypto("eth-usd"))
        else:
            message_data = massage_combine(item,"unused command")

        method = "sendMessage"
        try:
            result = requests.post(URL + method, data=message_data) # запрос на отправку сообщения
        except:
            print('Send message error')
            return False

        if not result.status_code == 200: # проверим статус пришедшего ответа
            return False
        
while True:
    
    try:
        upd_handling()
    except KeyboardInterrupt: # порождается, если бота остановил пользователь
        print('Interrupted by the user')
        break
    time.sleep(1)   
    


