from agent import listener
from composio.client.collections import TriggerCallback
import typing as t
from agent import crew, composio_toolset
from composio import Action
import dotenv
import os


dotenv.load_dotenv()
CLONE_DIR = os.environ.get("CLONE_DIR")

@listener.callback(filters={"trigger_name": "github_issue_added_event"})
def callback_function(event: TriggerCallback):
    '''This function will be called whenever the an issue is added to a github repository'''
    payload: dict = event.originalPayload

    # Extract necessary data from the payload
    repo_name: str = payload["repository"]["full_name"]
    issue_title: str = payload["issue"]["title"]
    issue_description: str = payload["issue"]["body"]
    issue_labels: t.List[dict] = payload["issue"]["labels"]

    # Check if the issue has `swe-solve` label
    should_solve: bool = any("swe-solve" == label["name"].lower() for label in issue_labels)

    if not should_solve:
        return
    
    print("Issue title:", issue_title)
    print("Issue description:", issue_description)

    crew.kickoff(
        inputs={
            "repo_name": repo_name,
            "issue_title": issue_title,
            "issue_description": issue_description,
            "CLONE_DIR": CLONE_DIR,
        }
    )
    response = composio_toolset.execute_action(
        action=Action.FILETOOL_GIT_PATCH,
        params={},
    )
    if response.get("error") and len(response["error"]) > 0:
        print("Error:", response["error"])
    elif response.get("patch"):
        print("=== Generated Patch ===\n" + response["patch"])
    else:
        print("No output available")


