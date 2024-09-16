import asyncio

from domain.server import Server


def async_run():
    server = Server()
    asyncio.run(server.listen())

if __name__ == "__main__":
    async_run()