"""
Task Execution Agent
Executes tasks by calling IDIT API and manages response handling
"""
from services.api_utils import get_api_utils
from agents.simple_ai_agent import get_simple_ai_agent
import json


class TaskExecution:
    """
    Agent responsible for executing tasks via IDIT API
    Handles API calls, response processing, and reply generation
    """

    updateContactUrl = ""

    def __init__(self):
        self.updateContactUrl = ""

    async def get_task_data(self, task_data):
        #category = task_data.get('category')  # entity in IDIT e.g. contact , policy, claim , accounting
        #task_type = task_data.get('taskType')  # update/get/remove/create
        entity_description = task_data.get('taskDescription')  # json from classification agent, in format entity:id
        entity = entity_description.split(":")[
            0]  # in case of more than one entity , it will keep the same format, e.g. contact:123 policy: 'abc'
        entity_id = task_data.get('contactExtId')

        entityDetails = get_api_utils().get_api(f"https://core-trunk-ci-qa.idit.sapiens.com:443/idit-web/api/contact/{entity_id}")
        # for k, v in entityDetails.items():
        # print(f"{k}:{v}")
        agent = get_simple_ai_agent()

        # שלח prompt ל-LLM
        response = await agent.generate_response(
            prompt="You are a JSON-processing assistant for API tasks. Your input includes a task type, a category, a free-text instruction, and a JSON object. Your job is to: Interpret the free text. Identify entities (such as name, city, street, number, phone, email, etc.) even if not explicitly labeled. Update or extract data in the JSON object accordingly.Output a valid JSON object — nothing else.Use common sense and linguistic cues to understand context. For example, detect that city name, street name, and number refers to a house number. based on the exact address modify the zip code,make sure to put all fields in english if required translate the input",
            context={
                'task_type': "PUT",
                'massage': "Update my name to  מלכה ברויאר and i moved apartment to '8 בעל התניא street Bnei Brak.",
                'JSON': json.dumps(entityDetails, indent=2)
            }
        )

        print(response)

    # getEntityBiId - decide which entity to fetch from DB (using api data list - in future MCP, Example below)

    # Api data list / MCP example
    # list = {
    #     "category": "contact", { }
    #     {"api": 'api/updateContact', {"contactId": entity_id,"contactName":"name" } , {'api/updatePolicy',{'contactId', entity "policyId":'123'}}} }


# Singleton instance


_task_execution = None


def get_task_execution_agent() -> TaskExecution:
    """Get or create task execution agent singleton"""
    global _task_execution
    if _task_execution is None:
        _task_execution = TaskExecution()
    return _task_execution
