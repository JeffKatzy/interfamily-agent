## MVC Langchain pattern implementation with chainlit 

* Currently deployed at https://internalfamilysystems.ai/

* Separates models from workflows (ie. views), to allow for separate logic from parsing and prompting.
* Both sequenced and non-sequenced responses achieved via routing.
* When sequenced workflow used, looks at skip logic of each question to see if step is complete.

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
