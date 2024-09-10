import asyncio

from domain.models.part import Part
from domain.server import Server
from domain.workflows.part_workflow import PartWorkflow


def build_server():
    workflows = [ PartWorkflow(Part()) ]
    return Server(workflows)

def async_run():
    server = build_server()
    asyncio.run(server.listen())

if __name__ == "__main__":
    async_run()