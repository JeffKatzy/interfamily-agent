import asyncio

from domain.models.part import Part
from domain.server import Server
from domain.workflows.part_workflow import PartWorkflow

workflows = [ PartWorkflow(Part()) ]
server = Server(workflows)
asyncio.run(server.listen())

asyncio.run(server.listen())

