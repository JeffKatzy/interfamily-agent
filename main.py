import asyncio

from dotenv import load_dotenv
from hypercorn.asyncio import serve
from hypercorn.config import Config
from quart import Quart, Response, jsonify, render_template, request
from quart_cors import cors

import domain.workflows.images.base_image as base_image
from domain.server import Server
from domain.store import clients

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
    user_id = '123';
    session_id = '456';
    async def generate_answer():
        prompt, next_message, session_id = server.get_prompt_and_inputs(text_input, user_id)
        async for chunk in server.invoke_stream(prompt, next_message, user_id, session_id):
            if chunk:
                yield f"data: {chunk}\n\n"
    return Response(generate_answer(), content_type='text/event-stream')

@app.route('/events')
async def sse():
    session_id = request.args.get('session_id')
    user_id = request.args.get('user_id')
    if not session_id:
        return jsonify({'error': 'session_id is required'}), 400
    
    base_image.add_to_queue(session_id)

    async def event_stream():
        while True:
            async for message in base_image.get_and_yield_message(session_id):
                yield message

    return Response(event_stream(), content_type='text/event-stream')


if __name__ == "__main__":
    config = Config()
    config.bind = ["0.0.0.0:8000"]
    app.debug = True

    asyncio.run(serve(app, config))