import os
import json
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai.types.chat.chat_completion import ChatCompletion
here = os.path.abspath(os.path.dirname(__file__))

def chat_completions_generate():
    filename="2a_generate_text_gai.json"
    fullpath=os.path.join(here, filename) 
    with open(fullpath,"r") as f:
        jsoned = json.load(f)
        completion = ChatCompletion(**jsoned)
    return completion

def chat_completions_stream():
    def streamer():
        filename="2b_stream_text_gai.json"
        fullpath=os.path.join(here, filename) 
        with open(fullpath,"r") as f:
            list = json.load(f)
            for chunk in list:
                chunk = ChatCompletionChunk(**chunk)
                chunk.extract = lambda: chunk.choices[0].delta.content
                yield chunk
    return (chunk for chunk in streamer())
    
def chat_completions_toolcall():
    filename="2c_toolcall_gai.json"
    fullpath=os.path.join(here, filename) 
    with open(fullpath,"r") as f:
        jsoned = json.load(f)
        completion = ChatCompletion(**jsoned)
    return completion

def chat_completions_json_schema():
    filename="2d_json_schema_gai.json"
    fullpath=os.path.join(here, filename) 
    with open(fullpath,"r") as f:
        jsoned = json.load(f)
        completion = ChatCompletion(**jsoned)
    return completion
