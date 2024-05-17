import asyncio
import threading
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from starlette.staticfiles import StaticFiles

from queues.gcp_pub_sub.gcp_pub_sub_consumer import GcpPubSubConsumer
from util.config_util import read_yaml_config

app = FastAPI()

origins = [
    "http://localhost:8082",
    "http://127.0.0.1:8082",
    "http://0.0.0.0:8082",
    "http://0.0.0.0:8081",
    "https://parallel-llm-queue-iu5vx2gsqa-uc.a.run.app",
    "https://parallel-llm-stream-iu5vx2gsqa-uc.a.run.app"
]

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = read_yaml_config("./message_queue_config.yaml")

consumer_handler = GcpPubSubConsumer(
    project=config.get('project'),
    subscription=config.get('subscription')
)

queue = None
event_loop = None


@app.on_event("startup")
async def startup_event():
    global queue, event_loop
    event_loop = asyncio.get_event_loop()
    queue = asyncio.Queue()

    # Start the message consumer in a separate thread
    threading.Thread(target=consumer_handler.consume_messages, args=(callback,), daemon=True).start()


@app.get("/")
async def main():
    return FileResponse('templates/index.html')


@app.get('/get_text_queue_stream')
async def get_text_queue_stream(request: Request):
    async def pubsub_stream():
        while True:
            message = await queue.get()
            yield message

    return StreamingResponse(pubsub_stream(), media_type='text/event-stream')


def callback(message):
    future = asyncio.run_coroutine_threadsafe(queue.put(message.data.decode('utf-8')), event_loop)
    try:
        future.result()  # Ensure the coroutine is scheduled properly
    except Exception as e:
        print(f"Error scheduling coroutine: {e}")
    message.ack()

if __name__ == "__main__":
    # Start the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8082, log_level="info")
