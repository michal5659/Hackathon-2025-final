"""
Simple AI Agent with LLM
"""
from typing import Dict, Any, Optional
import json
import re
from services.api_utils import get_api_utils
from openai import AzureOpenAI
from config.settings import settings

class ClassificationAgent:
    """
    Simple AI Agent with Azure OpenAI integration
    """

    def __init__(self):
        self.client = AzureOpenAI(
            api_key="",
            api_version="2024-02-01",
            azure_endpoint="https://moshe-m6dfn51l-eastus2.services.ai.azure.com"
        )
        self.deployment_name = "gpt-4o"

    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """
        Generate response using LLM

        Args:
            prompt: The prompt/question to send to LLM
            context: Additional context data

        Returns:
            Generated response text
        """
        try:
            # Build the full prompt with context
            valid_user_msg = self._get_email_message()
            unvalid_user_msg = self._build_unvalid_user_msg()
            system_msg = self._build_system_msg()
             # Call Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": system_msg
                    },
                    {
                        "role": "user",
                        "content": valid_user_msg
                    }
                ],
                temperature=0.7,
                max_tokens=800
            )

            # Extract the response
            result = response.choices[0].message.content
            
            # Extract only JSON from the response
            print(f"LLM Response generated successfully")
            json_result = self._extract_json(result)
            url = "https://core-trunk-ci-qa.idit.sapiens.com:443/idit-web/api/workflow/createTask"
            if(self.is_valid_classification(json_result)):
                print(f"Yes, valid classification create me task ! ")
                response = get_api_utils().post_api(url, json_result)
            else:
                print(f"No, invalid classification, do not create task ! ")

            return json_result



        except Exception as e:
            print(f"Error generating LLM response: {str(e)}")
            return "Sorry, I couldn't process your request at this time."

    def _build_prompt(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Build the full prompt with context"""
        if not context:
            return prompt

        context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
        return f"""Context:
{context_str}

User Request:
{prompt}

Please provide a helpful response."""

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """
        Extract JSON from model response, handling cases where the model
        includes explanatory text before or after the JSON.
        
        Args:
            text: The response text from the model
            
        Returns:
            Parsed JSON dictionary
        """
        try:
            # Try to parse the entire text as JSON first
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Look for JSON patterns in the text
        json_pattern = r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}'
        matches = re.findall(json_pattern, text)
        
        for match in matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
        
        # If no JSON found, return error message
        return {"result": "Not classified", "error": "No valid JSON found in response"}

    def is_valid_classification(self, json_result: Dict[str, Any]) -> bool:
        """
        Validate if the email classification is valid.

        Args:
            json_result: The JSON response from the LLM

        Returns:
            True if email is properly classified, False otherwise
        """
        # Check if email was not classified
        if json_result.get("result") == "Not classified":
            print(f"❌ Email NOT CLASSIFIED")
            print(f"Reason: {json_result.get('error', 'Does not meet classification criteria')}")
            return False

        # Check if required field contactExtId is present
        if not json_result.get("contactExtId"):
            print(f"❌ Email CLASSIFIED but INVALID - Missing contactExtId")
            print(f"Response: {json_result}")
            return False

        # Check if queueId is present
        if not json_result.get("queueId"):
            print(f"❌ Email CLASSIFIED but INVALID - Missing queueId")
            print(f"Response: {json_result}")
            return False

        # Email is valid
        print(f"✅ Email CLASSIFIED successfully")
        print(f"Contact ID: {json_result.get('contactExtId')}")
        print(f"Queue ID: {json_result.get('queueId')}")
        print(f"Task Description: {json_result.get('taskDescription')}")
        return True

    def _build_system_msg(self) -> str:
        return """You are an insurance expert. Your task is to classify incoming emails and, if they match specific criteria, generate a structured JSON object for task creation.

IMPORTANT: Respond with ONLY the JSON object. Do not include any explanation, text, or comments before or after the JSON.

Input Format:
Each email includes:
- from: string — the sender of the email
- subject: string — the subject line of the email
- body: string — the body content of the email

Classification Criteria:
An email is considered classified if it shows clear intent to modify contact details. This includes:
- Mentions of updating contact details (address, phone number, email, personal info)
- Requests to change or correct contact-related data
- References to a contact record being edited, updated, or needing attention

Use semantic understanding, not just keyword matching.

If Classified, Generate the Following JSON (and ONLY this JSON):
{
  "queueId": 10886,
  "contactExtId": "string",
  "dueOn": "2025-11-07T12:09:35.827Z",
  "updateVersion": 0,
  "taskDescription": "Contact: [contact reference]",
  "priority": 1,
  "followUpSuperType": 0,
  "startHandlingOn": "2025-11-07T12:09:35.827Z",
  "consequences": 0,
  "id": 0,
  "remarks": "string",
  "taskCategory": 0
}

Extraction Logic for contactExtId:
You must extract contactExtId from the email using one of the following patterns:
1. Explicit ID: Look for phrases like "Contact ID:", "contactExtId =", "contact #", "contact id", "contact number"
2. Email or Name Reference: If an email address or full name is mentioned and clearly refers to the contact, use that
3. CRM-style Reference: If the email refers to a contact in a system (e.g., "contact # 45678"), extract the number

If no valid contactExtId is found, the email is not classified.

Task Description Logic:
Set taskDescription as: "Contact: [contact reference]"
Extract the contact reference in this order:
1. From the subject
2. If not found, from the body
3. If still not found, use the from field

Remarks Logic:
Set remarks to the actual request found in the email body — ideally the sentence or paragraph that describes what the sender wants done.

If Not Classified:
Return ONLY: {"result": "Not classified"}
"""

    def _build_valid_user_msg(self) -> str:
        return """"
        {
          "from": "noa.benari@insureplus.com",
          "subject": "Change of address for Contact ID: 415089",
          "body": "Hello,\n\nPlease update the contact information for Contact ID: 415089. The new address is 45 Herzl Street, Tel Aviv, 67890.\n\nThank you,\nNoa"
        }
         """
    def _build_unvalid_user_msg(self) -> str:
        return """"
        {
          "from": "lior.cohen@insureplus.com",
          "subject": "Meeting reschedule request",
          "body": "Hi,\n\nCan we reschedule our meeting regarding the new product launch to next Wednesday at 10am?\n\nThanks,\nLior"
        }
         """

    def _get_email_message(self) -> str:
        return""" {
            "from": "yael.rubin@insureplus.com",
            "subject": "Correction needed for Contact ID: 55678",
            "body": "Hi,\n\nPlease update the email address for Contact ID: 55678. The correct email is yael.rubin.new@insureplus.com.\n\nThanks,\nYael"
        }"""
# Singleton
_classification_agent = None


def get_classification_agent() -> ClassificationAgent:
    """Get or create classification AI agent singleton"""
    global _classification_agent
    if _classification_agent is None:
        _classification_agent = ClassificationAgent()
    return _classification_agent
