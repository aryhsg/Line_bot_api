# 🤖 Line Bot API for n8n Webhook

## ✨ 專案簡介
本專案提供一個部署在雲端的 **Line Bot API 端點**，專門用於接收來自 Line 聊天室的訊息，並將其內容**轉傳**至 **n8n 工作流程的 Webhook** 進行後續的業務邏輯處理。

這個設計模式實現了 Line 訊息的靈活處理，將 Line 平台的接收與 n8n 的強大自動化能力結合。

---

## 🛠️ 具體運作流程

### 實現 Line 訊息 **接收**、**轉傳**與 **自動化處理** 的完整流程：

1.  **用戶發送訊息**：Line 用戶在聊天室中發送一則訊息。
2.  **Line 官方伺服器**：訊息送達 Line 官方伺服器。
3.  **Line Bot API (本專案)**：Line 官方伺服器將訊息導向預先設定的 Line Bot Webhook URL（即本專案的雲端端點）。
4.  **轉傳至 n8n**：本專案接收到 Line 訊息的 JSON Payload 後，會立即將該內容以 **POST 請求** 的方式轉傳（或稱代理）至指定的 `CLAWCLOUD_WEBHOOK_URL`。
5.  **n8n 處理**：n8n 工作流程（Workflow）被 Webhook 觸發，並開始執行定義好的自動化步驟（例如：資料庫存儲、呼叫其他 API、或是發送回覆訊息等）。

---

## 🚀 部署與架設

本專案旨在提供一個**實際可用**的雲端服務，因此選用了 **Render** 平台進行部署。

### 💻 部署細節

| 項目 | 說明 |
| :--- | :--- |
| **部署平台** | **Render** (或其他支援持續部署的雲服務，如 Heroku, Vercel 等) |
| **主要目的** | 取得一個 Line 平台可存取的 **公開網域名稱/URL**，作為 Line Bot 的 Webhook URL。 |

### 🌐 服務保持上線機制 (Keep-Alive)

由於部分免費/低成本雲服務（如 Render 的免費方案）可能會在一段時間沒有流量後進入休眠狀態，這會導致 Line 訊息無法即時被處理。

**為了保證服務的**高可用性**：**
* **機制**：利用 **n8n** 內建的 **Cron/Interval 節點**（或其他定時執行服務）。
* **動作**：設定 n8n **定時**對 Render 部署的 API 網址發送 **Ping 請求**。
* **效果**：確保 Render 上的服務持續保持**上線 (Active)** 狀態，保證使用者能**隨時**在 Line 傳遞訊息並得到即時的自動化回覆。

---

## ⚙️ 環境變數 (Environment Variables)

為了成功運行和連接 Line 平台與 n8n，您需要在部署時設定以下環境變數：

| 變數名稱 | 說明 | 範例/用途 |
| :--- | :--- | :--- |
| `SECURITY_TOKEN` | 傳遞到 n8n 的 request header 的 **X-Security-Token**。 | `xxxxxxxx(內容自訂)` |
| `CLAWCLOUD_WEBHOOK_URL` | n8n 工作流程中 **Webhook 節點** 的完整 URL。 | `https://n8n-xxxxx.clawcloudrun/webhook/abcdefg` |

---
