import requests
import asyncio
from telegram import Bot

TOKEN = "ENTER_YOUR_BOT_TOKEN"
CHAT_ID = "ENTER_YOUR_CHANNEL_CHAT_ID"

bot = Bot(token=TOKEN)

url = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live"

old_data_id = ''

def getData():
    req = requests.get(url)
    if req.status_code == 200:
        data = req.json()
        last_data = data.get("result", [])[0]
         
        return last_data
    
    else:
        print("İstek başarısız oldu. Kod:", req.status_code)



async def data_check():
    global old_data_id
    while True:
        data = getData()
        if data['_id'] != old_data_id:
            print(True)
            old_data_id = data['_id']
            
            lon = data['geojson']['coordinates'][1]
            lat = data['geojson']['coordinates'][0]

            caption = f"""
Deprem Bölgesi: {data['title']}\n
Tarih: {data['date']}\n
Derinlik: {data['depth']}
            """
            await bot.send_location(chat_id=CHAT_ID, latitude=lat, longitude=lon)
            await bot.send_message(chat_id=CHAT_ID, text=caption)
        await asyncio.sleep(60)  # Her 60 saniyede bir çalış

async def main():
    while True:
        await data_check()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
