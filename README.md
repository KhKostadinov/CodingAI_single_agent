This is a bit more complex agent (just a little bit) - I decided to explore the ways of creating a coding agent with Pydantic AI. 
It appears to be relatively successful having in mind it is very basic and does not have the capabilities of its most famous 
"cousins" like Opencode, Hermes, etc. - it can not create virtual environments, execute scripts, perform unit testing and so on. 
Below is a list of the tech stack:
  - Python 3.14
  - Pydantic AI
  - Ollama as an LLM provider
  - Model - Qwen3.8:27b
Main difference here in terms of tools is that I built them as functions decorated by the agent object (CodeMaster in this project) instead of listing them when defining the agent.
I've used tool_plain because I didn't use dependency injection here.

I've faced two main obstacles in this project:
  1. Model incompatibility - initially I planned to use Qwen3-coder but it isn't compatible Pydantic AI for Ollama locally and returns an xml-like answer instead of actual
     tool execution. The reason for this is that Pydantic AI is expecting a json object instead of the provided xml so the solution was to change the LLM.
  2. Timeout - the agent works well for shorter/smaller tasks but for bigger tasks more time is needed for processing the context/context history and
     "pydantic_ai.exceptions.ModelAPIError: Request timed out." was often thrown as error. I've fixed this by setting timeout=300.0 (i.e. 5 minutes) when defining the agent.

So, to test the coding agent abilities I asked it to create simple Flask register/login template: 

<img width="1637" height="362" alt="prompt" src="https://github.com/user-attachments/assets/e1d236cd-74a0-4526-a964-d42ec58486f4" />

And although there are some things to be updated (i.e. the register button is not visible at the bottom of the register page) the result is quite satisfying.

Login page:

<img width="632" height="883" alt="welcome_screen" src="https://github.com/user-attachments/assets/e5fb3420-26ce-46ea-81fa-ea3663240667" />

Register page:

<img width="633" height="883" alt="register" src="https://github.com/user-attachments/assets/1b5fdddc-5f8a-4941-8562-e9e7cb9d71cf" />

Dashboard after login:

<img width="1495" height="770" alt="dashboard" src="https://github.com/user-attachments/assets/e948a1bb-8aaf-4d1d-9b43-a0c6f4d97ce8" />

