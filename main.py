import asyncio

from dotenv import load_dotenv
from hypercorn.asyncio import serve
from hypercorn.config import Config
from openai import OpenAI
from quart import Quart, Response, render_template, request
from quart_cors import cors

from domain.server import Server

load_dotenv()

app = Quart(__name__)
app = cors(app)

server = Server()

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/answer', methods=['GET','POST'])
async def answer():
    
    data = await request.get_json()
    text_input = data.get('message')
    user_id = '1'
    async def generate_answer():
        prompt, next_message, session_id = server.get_prompt_and_inputs(text_input, user_id)
        async for chunk in server.invoke_stream(prompt, next_message, user_id, session_id):
            if chunk:
                yield f"data: {chunk}\n\n"
    return Response(generate_answer(), content_type='text/event-stream')


if __name__ == "__main__":
    config = Config()
    config.bind = ["0.0.0.0:8000"]

    asyncio.run(serve(app, config))