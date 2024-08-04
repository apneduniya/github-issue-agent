"""CrewAI SWE Agent"""

import os

import dotenv
from crewai import Agent, Crew, Process, Task
# from custom_tools import say
from langchain_openai import ChatOpenAI
from prompts import BACKSTORY, DESCRIPTION, EXPECTED_OUTPUT, GOAL, ROLE

from composio_crewai import Action, App, ComposioToolSet, WorkspaceType


# Load environment variables from .env
dotenv.load_dotenv()

# Initialize tool.
openai_client = ChatOpenAI(
    api_key=os.environ["OPENAI_API_KEY"],  # type: ignore
    model="gpt-4-turbo",
)
composio_toolset = ComposioToolSet(workspace_config=WorkspaceType.Host())

# Get required tools
tools = [
    *composio_toolset.get_tools(
        apps=[
            App.FILETOOL,
            App.SHELLTOOL,
        ]
    ),
    # *composio_toolset.get_actions(
    #     actions=[
    #         say,  # This is just here as an example of a custom tool, you can remove it
    #     ]
    # ),
]

# Define agent
agent = Agent(
    role=ROLE,
    goal=GOAL,
    backstory=BACKSTORY,
    llm=openai_client,
    tools=tools,
    verbose=True,
)

task = Task(
    description=DESCRIPTION,
    expected_output=EXPECTED_OUTPUT,
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    process=Process.sequential,
    full_output=True,
    verbose=True,
    cache=False,
    memory=True,
)



listener = composio_toolset.create_trigger_listener() 

