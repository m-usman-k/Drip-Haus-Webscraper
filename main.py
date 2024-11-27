import aiohttp, asyncio, os
import requests, json, time, re

import pandas as pd

from concurrent.futures import ThreadPoolExecutor


# Globals:
FIELDS = [
    "Creator Name",
    "Profile URL",
    "About Section",
    "No Of Followers",
    "No Of Thanks",
    "Country"
]

OUTPUT_FILE_NAME = "./Drip" + str(int(time.time())) + ".xlsx"
OUTPUT_SHEET_NAME = "Drip"

# Any useful functions:
def scrape_each_user(df , index , slug):
    print(f"{index} | {slug}")

def identify_country(text):
    with open("./countries.json" , "r") as file:
        country_names = json.load(file)

        for country in country_names:
            if re.search(rf'\b{re.escape(country)}\b', text, re.IGNORECASE):
                return country
            
        return None

async def get_all_userdata():
    url = 'wss://drip.haus/drip/websocket?vsn=2.0.0'
    
    headers = {
        'Sec-WebSocket-Extensions': 'permessage-deflate',
        'Sec-WebSocket-Key': 'LzyNc5teELEMWSliCvrG7w==',
    }

    # Performing the handshake:
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url, headers=headers) as ws:
            print(f"🟢 | Connected to {url}")

            message = ["3","3","drip","phx_join",{"bearer":"56924e08-0db4-45e2-bd64-cf8547f09c00","anonId":"455f499e-c16d-4eb2-baff-dba09aa9979e","ua":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"}]
            json_message = json.dumps(message)
            await ws.send_str(json_message)


            message = ["3","6","drip","get_channels",{}]
            json_message = json.dumps(message)
            await ws.send_str(json_message)

            while True:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        try:
                            if len(json.loads(msg.data)[-1]["response"]["results"]) > 50:
                                with open("./userdata.json" , "w" , encoding="utf-8") as file:
                                    json.dump(json.loads(msg.data) , file , indent=4)
                                
                                return
                        except Exception as e:
                            pass
                        
                    elif msg.type == aiohttp.WSMsgType.PING:
                        print("🟢 | Received PING, sending PONG")
                        await ws.pong()

                    elif msg.type == aiohttp.WSMsgType.PONG:
                        print("🟢 | Received PONG")

                    elif msg.type == aiohttp.WSMsgType.CLOSE:
                        print("🔴 | Connection closed by server")
                        break

                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        print("🔴 | Error occurred")
                        break

                await asyncio.sleep(5)

# Main process exection:
if __name__ == "__main__":
    asyncio.run(get_all_userdata())
    
    if os.path.exists("./userdata.json"):
        df = pd.DataFrame()

        for field in FIELDS:
            df[field] = None
            
        all_userdata = []
        with open("./userdata.json" , "r") as file:
            all_userdata = json.load(file)[-1]["response"]["results"]

        all_threads = []
        with ThreadPoolExecutor(max_workers=10) as pool:
            for index, user_data in enumerate(all_userdata):
                thread = pool.submit(scrape_each_user, df , index , user_data["slug"])
        
        with pd.ExcelWriter(OUTPUT_FILE_NAME , mode="w") as writer:
            df.to_excel(excel_writer=writer , sheet_name=OUTPUT_SHEET_NAME , index=False)
    else:
        print(f"🔴 | Error getting all userdata")

