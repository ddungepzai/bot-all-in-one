# -*- coding: utf-8 -*-
import os
import time
import subprocess
import json

TOKEN = "8857086218:AAEUbuZEmt-ow5sbCLp0vL2vYL0Q5VcyQpc"
MY_CHAT_ID = "8976170772"  # Chỉ nhận lệnh từ Chat ID của bạn
AUDIO_PATH = "troll.mp3"

def send_telegram_message(chat_id, text):
    try:
        msg_url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
        subprocess.check_output([
            "curl", "-s", "-X", "POST", msg_url,
            "-d", "chat_id=" + str(chat_id),
            "-d", "text=" + text
        ])
    except Exception as e:
        print("Loi gui tin nhan:", e)

def get_latest_offset():
    try:
        url = "https://api.telegram.org/bot" + TOKEN + "/getUpdates?limit=1"
        output = subprocess.check_output(["curl", "-s", url])
        data = json.loads(output.decode('utf-8'))
        results = data.get("result", [])
        if results:
            return results[-1]["update_id"] + 1
    except:
        pass
    return 0

def run_bot():
    print("Bot da san sang...")
    offset = get_latest_offset()
    url = "https://api.telegram.org/bot" + TOKEN + "/getUpdates"
    
    while True:
        try:
            full_url = url + "?offset=" + str(offset) + "&timeout=30"
            output = subprocess.check_output(["curl", "-s", full_url])
            data = json.loads(output.decode('utf-8'))
            
            for result in data.get("result", []):
                offset = result["update_id"] + 1
                message = result.get("message", {})
                chat_id = str(message.get("chat", {}).get("id", ""))
                text = message.get("text", "")
                
                # CHỈ XỬ LÝ KHI ĐÚNG LÀ BẠN NHẮN LỆNH /play
                if chat_id == MY_CHAT_ID and text.strip() == "/play":
                    send_telegram_message(MY_CHAT_ID, "Da kich hoat")
                    subprocess.Popen(["afplay", AUDIO_PATH])
                        
        except Exception as e:
            print("Loi:", e)
            time.sleep(5)
        time.sleep(1)

if __name__ == "__main__":
    run_bot()