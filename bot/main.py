import requests
import json
import time
import ../config

TOKEN = config.TOKEN
URL     = "https://api.telegram.org/"
LIMIT   = 0 
GETUPD_method  = "getUpdates"
POSTMSG_method = "sendMessage"

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
    response = requests.get(URL + TOKEN +"/"+ method)
    decoded = response.json()
    return json.dumps(decoded, indent=4)

def fetch_crypto(type):
    url_crypto = "https://api.cryptonator.com/api/ticker/"
    res = requests.get(url_crypto + type)
    if res.status_code==200:
        return res.json()['ticker']['price']

def get_command(text):
    if not text.find("/start")==-1:
        return "start"
    elif not text.find("/btc")==-1: 
        return "btc"
    elif not text.find("/eth")==-1:
        return "eth"
    #можно либо продолжить поиск уникальных команд, либо брать любой набор символов после слеша и пытаться получить ответ от API cryptonator
    
def massage_combine(item,text):
    message_data = { 
    'chat_id': item['message']['chat']['id'],               # куда отправляем сообщение
    'text': text,                                         # само сообщение для отправки 
    'reply_to_message_id': item['message']['message_id'],   # если параметр указан, то бот отправит сообщение в reply
    'parse_mode': 'HTML' 
    }
    return message_data

def upd_handling(offset):

    par = {'limit': LIMIT, 'offset': offset, 'timeout':3}
    print(par)
    try:
        result = requests.get(URL + TOKEN +"/"+ GETUPD_method, params=par)
    except:
        print('Error getting updates')
        return offset

    if not result.status_code == 200: 
        return offset
    if not result.json()['ok']: 
        return offset

    udates = result.json()['result']

    for item in udates:
         
        new_offset = item['update_id']+1
        
        if 'message' not in item or 'text' not in item['message']: 
            print('Unknown message')
            continue

        # сообщение из чата
        message_id  = item['message']['message_id']
        text        = item['message']['text']
        print(message_id, text)

        # сообщение в ответ
        cmd = get_command(text)
        if cmd=="start":
            message_data = massage_combine(item,bot_about()) 
        elif cmd=="btc" or cmd=="eth":
            message_data = massage_combine(item,fetch_crypto(cmd+"-usd"))
        else:
            message_data = massage_combine(item,"unused command")

        try:
            result = requests.post(URL + TOKEN +"/"+ POSTMSG_method, data=message_data) # запрос на отправку сообщения
        except:
            print('Send message error')
            return offset

        if not result.status_code == 200: # проверим статус пришедшего ответа
            return offset
        
        return new_offset

offset  = 0    
while True:  
    try:
        offset = upd_handling(offset)
    except KeyboardInterrupt: # порождается, если бота остановил пользователь
        print('Interrupted by the user')
        break
    time.sleep(1)   
    


