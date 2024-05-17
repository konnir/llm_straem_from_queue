import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from llm.llm_open_ai.llm_open_ai import LlmOpenAi
from queues.gcp_pub_sub.gcp_pub_sub_producer import GcpPubSubProducer
from util.config_util import read_yaml_config, read_text_file

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_handler = LlmOpenAi()

SYSTEM_SONG_PROMPT = read_text_file("./prompts/songs_system_prompt.txt")

config = read_yaml_config("./message_queue_config.yaml")

producer_handler = GcpPubSubProducer(
    project=config.get('project'),
    topic=config.get('topic')
)


@app.get("/")
async def main():
    return FileResponse('templates/index.html')

@app.post('/get_text_stream')
async def get_text_stream(request: Request):
    form_data = await request.form()
    text = form_data.get('topic', 'dog')

    async def generate_tokens():
        print("generate")
        try:
            completion = llm_handler.llm_compilation_stream(
                text=text,
                system=SYSTEM_SONG_PROMPT,
                model='gpt-3.5-turbo'
            )
            for chunk in completion:
                if getattr(chunk, 'choices', None):
                    delta_text = chunk.choices[0].delta.content if getattr(chunk.choices[0].delta, 'content', None) else ""
                    delta_text_bytes = delta_text.encode('utf-8')
                    if delta_text is not None:
                        producer_handler.publish_messages([delta_text_bytes])
                        yield delta_text_bytes
        except Exception as e:
            print('error')
            yield str(e).encode('utf-8')

    return StreamingResponse(generate_tokens(), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="info")
