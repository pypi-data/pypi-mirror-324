from rq import get_current_job
from plurally.models.node import Node


class TextOutput(Node):

    class InputSchema(Node.InputSchema):
        content: str

    class InitSchema(Node.InitSchema): ...

    class OutputSchema(Node.OutputSchema): 
        content: str

    def forward(self, node_input):
        current_job = get_current_job()
        self.outputs = {"content": node_input.content}
        if current_job:
            current_job.meta["output"] = {"content": node_input.content}
            current_job.save_meta()

