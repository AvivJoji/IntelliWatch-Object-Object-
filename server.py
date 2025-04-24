import asyncio
from aiohttp import web

clients = []

# Serve HTML file
async def index(request):
    return web.FileResponse('index.html')

# WebSocket handler
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    clients.append(ws)
    print("🟢 Client connected.")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                print("📥 Received:", msg.data)
                # Broadcast to all clients
                for client in clients:
                    if not client.closed:
                        await client.send_str(msg.data)
    finally:
        clients.remove(ws)
        print("🔴 Client disconnected.")

    return ws

# Web app config
app = web.Application()
app.router.add_get('/', index)
app.router.add_get('/ws', websocket_handler)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=3000)