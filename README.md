## MVC Langchain pattern implementation with chainlit 

* Currently deployed at https://internalfamilysystems.ai/

## Architecture:
* Generic logic (mainly) abstracted to `lib` and custom logic in `domain`.  Goal is to just add new models and workflows and app will:
    1. Routes between sequenced workflow and non-sequenced responses.
    2. When workflow used, find next step by looking at skip logic of each question to see if step is complete (with help of `workflow_utils`).
    3. Allow for separate logic from parsing (in models) and prompting (in workflows)
    
## To run:

* `git clone https://github.com/JeffKatzy/mvc-langchain`
* `cd mvc-langchain`
* `poetry shell`
* `poetry install`
* `mv .env.example .env`
* Add your openai api key, and add abs path to the project in PYTHON_PATH
* `chainlit run app.py`

Or run backend with:
* `python3 -i backend_runner.py`

### Todo:

* Potentially refactor more with langchain
    * Refactor with langgraph state?  Does this slow it down?
* Still should look into Zep for output parsing
* Look at Cerebras for latency
