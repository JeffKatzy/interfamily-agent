import asyncio
import time

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
app = cors(app, allow_origin="http://localhost:3000")
server = Server()

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/answer', methods=['GET','POST'])
async def answer():
    data = await request.get_json()
    text_input = data.get('message')
    user_id = data.get('user_id')
    session_id = data.get('session_id')
    

    async def generate_answer(user_id, session_id):
        start_time = time.time()
        prompt, next_message, session_id = await server.get_prompt_and_inputs(text_input, user_id, session_id)
        print("done getting prompt and inputs", session_id)
        first_chunk = True
        async for chunk in server.invoke_stream(prompt, next_message, user_id, session_id):
            if first_chunk:
                first_chunk = False
                end_time = time.time()
                print(f"first chunk took {end_time - start_time:.2f} seconds")
                
            if chunk:
                yield f"data: {chunk}\n\n"
    return Response(generate_answer(user_id, session_id), content_type='text/event-stream')

@app.route('/events')
async def sse():
    session_id = request.args.get('session_id')
    user_id = request.args.get('user_id')
    if not session_id:
        return jsonify({'error': 'session_id is required'}), 400
    base_image.add_to_queue(session_id, clients)

    async def event_stream():
        while True:
            keep_alive_interval = 15
            last_message_time = time.time()
            async for message in base_image.get_and_yield_message(session_id, clients):
                yield message

            if time.time() - last_message_time > keep_alive_interval:
                yield "data: keep-alive\n\n"
                last_message_time = time.time()
            await asyncio.sleep(.5)
    return Response(event_stream(), content_type='text/event-stream')

if __name__ == "__main__":
    config = Config()
    config.bind = ["0.0.0.0:8000"]
    app.debug = True

    asyncio.run(serve(app, config))