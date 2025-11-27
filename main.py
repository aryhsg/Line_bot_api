import os
import httpx # 👈 使用非同步 HTTP 客戶端
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv

load_dotenv()
# 應用程式實例命名為 app
app = FastAPI()

# --- 從環境變數中讀取設定 ---
N8N_WEBHOOK_URL = os.environ.get('N8N_WEBHOOK_URL')
SECURITY_TOKEN = os.environ.get('N8N_SECURITY_TOKEN')
# ----------------------------
if not N8N_WEBHOOK_URL:
    raise ValueError("FATAL: N8N_WEBHOOK_URL environment variable is not set!")
# 註冊 POST 路由，用於接收 LINE Webhook
@app.post("/callback")
# 使用 async 關鍵字，並從 Request 物件中讀取數據
async def line_webhook_forwarder(request: Request):
    
    # 1. 取得 LINE 傳來的原始請求內容 (Body)
    # 必須使用 await request.body() 來處理非同步數據流
    body = await request.body()
    
    # 2. 建立轉發所需的 Header 字典
    forward_headers = {
        # 這是 n8n 要求的安全密鑰
        'X-Security-Token': SECURITY_TOKEN, 
        
        # 保持 Content-Type 以便 n8n 正確解析
        'Content-Type': 'application/json' 
    }
    
    # 3. 使用 httpx 進行非同步轉發
    try:
        # httpx.AsyncClient 適合單次發送
        async with httpx.AsyncClient() as client:
            response = await client.post(
                N8N_WEBHOOK_URL,
                content=body, # FastAPI/httpx 使用 content 或 data 都可以傳輸原始 bytes
                headers=forward_headers 
            )
            
        # 4. 檢查 n8n 的回覆狀態 (可選，用於紀錄錯誤)
        if response.status_code != 200:
             # 紀錄 n8n 處理失敗的訊息
             print(f"n8n returned non-200 status: {response.status_code}. Response: {response.text}")
             
    except Exception as e:
        # 紀錄網路或轉發錯誤
        print(f"An error occurred during forwarding to n8n: {e}")
        
    # 5. 立即回覆給 LINE 伺服器 (必須是 200 OK，使用 PlainTextResponse 確保回應乾淨)
    return PlainTextResponse("OK", status_code=200)

@app.get("/callback")
def read_root():
    return PlainTextResponse("OK", status_code=200)

if __name__ == "__main__":
    import uvicorn
    # 本地測試時，使用 uvicorn 啟動
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
