import asyncio

from dotenv import load_dotenv
from hypercorn.asyncio import serve
from hypercorn.config import Config
from openai import OpenAI
from quart import Quart, Response, render_template, request
from quart_cors import cors

from backend_runner import build_server

load_dotenv()

app = Quart(__name__)
app = cors(app)

server = build_server()

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/answer', methods=['GET','POST'])
async def answer():
    data = await request.get_json()
    message = data.get('message')
    
    async def generate_answer():
        async for chunk in server.route_from(message):
            if chunk:
                yield f"data: {chunk}\n\n"
    return Response(generate_answer(), content_type='text/event-stream')


if __name__ == "__main__":
    config = Config()
    config.bind = ["0.0.0.0:8000"]

    asyncio.run(serve(app, config))