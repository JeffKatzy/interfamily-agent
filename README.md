## MVC Langchain pattern implementation with chainlit 

* Currently deployed at https://internalfamilysystems.ai/
* AWS Fargate/ECS/Gateway

## Start it up:

* `git clone https://github.com/JeffKatzy/mvc-langchain`
* `cd mvc-langchain`
* `poetry shell`
* `poetry install`
* `mv .env.example .env`
* Add your openai api key, and add abs path to the project in PYTHON_PATH
* `chainlit run app.py`

Or run backend with:
* `python3 -i backend_runner.py`

## Architecture:

<img src="https://jigsaw-labs-student.s3.amazonaws.com/request-response.png" width="90%"/>


Incoming user messages are routed to either a general response or a sequenced workflow.
A *workflow* is the sequence of steps, that the agent responds with individually.  It is essentially a ViewModel.  Each application may have many workflows.

Each step in a workflow has it's own *skip* logic that indicates if the step is already complete.  This is often a combination of the state of the underlying model (eg. has the application parsed the related information) and the workflow itself (have we asked enough times.) 

For example, the bot gets the next step by checking off the steps in sequence to look if the `skip` lambda function returns True.  It's looking at the related model  to see if it has the information it needs.

```python
class PartWorkflow(BaseWorkflow):
    _model: Part

    find_part: WField = WField(prompt="Ask if there's a feeling, struggle, thought pattern, or part they need help with.",
        skip=lambda view: bool(view._model.part))
    assess_awareness: WField = WField(prompt = "Thank them, mirror using parts language.  Then ask if they're aware of this part and how they sense or are aware of the part.",
                        skip=lambda view: bool(view._model.aware_of_part))

class Part(BaseModel):
    part: str = Field("",
        description="A feeling, struggle, thought pattern, or part they encounter.")
```

The `BaseWorkflow` class's `get_next_message` function will call each `skip` procedure in sequence, until reaching what is yet to be completed.

Additional workflows are added by adding them to the `Server`.  

```python
workflows = [ PartWorkflow(Part())]
server = Server(workflows)
asyncio.run(server.listen())
```

### Todo:

* Potentially refactor more with langchain
    * Refactor with langgraph state?  Does this slow it down?
* Still should look into Zep for output parsing
* Look at Cerebras for latency
