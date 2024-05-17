from abc import ABC
from dotenv import load_dotenv
from openai import OpenAI, Stream


class LlmOpenAi():
    """ Specific handler for opne-ai LLMs """

    def __init__(self):
        load_dotenv()
        self.client: OpenAI = OpenAI()

    def llm_compilation_stream(self, text: str, system: str, model: str) -> Stream:
        """ Open compilation - an opneai.stram object will be returned"""
        return self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {'role': "user", "content": text}
            ],
            temperature=1,
            stream=True
        )

if __name__ == '__main__':
    handler = LlmOpenAi()
    text = "life at the edge of the world"
    system_prompt = "You are a gothic song composer, write a gothic song about the description / topic below."
    compilation = handler.llm_compilation_stream(
        text=text,
        system_prompt=system_prompt,
        model="gpt-3.5-turbo"
    )

    # print compilation
    for chunk in compilation:
        if getattr(chunk, 'choices', None):
            # delta_text = chunk.choices[0].delta.content.encode('utf-8') if getattr(chunk.choices[0].delta, 'content', None) else ""
            delta_text = chunk.choices[0].delta.content if getattr(chunk.choices[0].delta, 'content', None) else ""
            if delta_text is not None:
                    print(delta_text, end="")
            if len(delta_text) == 0:
                if chunk.choices[0].finish_reason is not None:
                    print(f"\n\nFINISH due to: {chunk.choices[0].finish_reason}\n")

