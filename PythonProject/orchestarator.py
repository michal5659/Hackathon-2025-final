import asyncio
from typing import Dict, Any
from agents import get_classification_agent, get_task_execution_agent
from agents import get_task_execution_agent
# from services import get_message_pull_service
# from utils.logger import get_logger
from config.settings import settings


# logger = get_logger(__name__)


class Orchestrator:
    """
    Main orchestrator for the AI Multi-Agent System
    Coordinates message flow through classification, task creation, and execution
    """

    async def start(self):
        print("Starting AI Multi-Agent Orchestration System")
        message = {
            "message_id": '1',
            "title:": 'update Address',
            "content": 'HI, I want to update my new addres: 3 Broyer st. BB. thanks, malka blau.',
            "sender": 'malka.blau@sapiens.com',
            "channel": 'manual',
        }

        await self.process_message(message)

    def __init__(self):
        self.classification_agent = get_classification_agent()
        # self.task_creation_agent = get_task_creation_agent()
        self.task_execution_agent = get_task_execution_agent()
        # self.message_service = get_message_pull_service()
        self.max_concurrent_tasks = settings.app.max_concurrent_tasks
        self.semaphore = asyncio.Semaphore(self.max_concurrent_tasks)

    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single message through the full pipeline

        Args:
            message: Standardized message dictionary

        Returns:
            Processing result with status and response
        """
        async with (self.semaphore):
            try:
                print(f"Processing message {message.get('message_id')} from {message.get('channel')}")

                # Stage 1: Classification
                # classification_result = await self._classify_message(message)

                # if not classification_result:
                #   print("Classification failed")
                #    return self._create_error_result(message, "Classification failed")

                # Stage 2: Task Creation
                # task_data = await self._create_task(classification_result, message)

                # if not task_data:
                #   print("Task creation failed")
                #    return self._create_error_result(message, "Task creation failed")

                # Stage 3: Task Execution
                task_data = {
                    "queueId": 10886,
                    "contactExtId": "617259",
                    "dueOn": "2025-11-07T12:09:35.827Z",
                    "updateVersion": 0,
                    "taskDescription": "Contact: [contact reference]",
                    "priority": 1,
                    "followUpSuperType": 10000,
                    "startHandlingOn": "2025-11-07T12:09:35.827Z",
                    "consequences": 10000,
                    "id": 0,
                    "remarks": "string",
                    "taskCategory": 10000
                }

                response= await  get_task_execution_agent().get_task_data(task_data)
            except Exception as e:
                print(f"Error processing message {message.get('message_id')}: {str(e)}")
                return {"status": "failed", "response": None}


_orchestrator = None


def get_orchestrator() -> Orchestrator:
    """Get or create orchestrator singleton"""
    print("getting orchestrator...")
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = Orchestrator()
    return _orchestrator
