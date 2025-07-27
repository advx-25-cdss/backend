import os
import json
from typing import List, Optional
from openai import OpenAI
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv


# --- 1. Pydantic Models for Structured Output ---
class Test(BaseModel):
    """A single recommended diagnostic test."""

    test_name: str
    notes: Optional[str] = None


class TestRecommendations(BaseModel):
    """A list of recommended tests."""

    recommendations: List[Test]


# --- 2. Function to Call OpenAI API ---
def get_test_recommendations(transcription: str) -> Optional[TestRecommendations]:
    """
    Analyzes a transcription and returns structured test recommendations.

    Args:
        transcription: The string transcription of a doctor-patient encounter.

    Returns:
        A Pydantic object with a list of recommended tests, or None on error.
    """
    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    use_ppio = os.getenv("PPIO", 1)
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file.")
        return None

    if use_ppio:
        client = OpenAI(api_key=os.getenv("PPIO_KEY"), base_url="https://api.ppinfra.com/v3/openai")
    else:
        client = OpenAI(api_key=api_key)

    # --- The Core Prompt Engineering ---
    system_prompt = f"""
    You are an expert Clinical Decision Support System (CDSS) assistant that responds in simplified chinese. 
    Your task is to analyze the following doctor-patient encounter transcription and recommend a set of diagnostic tests.

    **Key Instructions:**
    1.  **Balance Accuracy and Cost:** The recommendations must balance diagnostic accuracy with resource consumption. Prioritize essential, cost-effective tests that provide the most value for confirming or ruling out likely diagnoses.
    2.  **Justify Recommendations:** For each test, provide a brief, clear note in the `notes` field explaining *why* it is recommended (e.g., "To rule out acute coronary syndrome", "To check for signs of infection").
    3.  **Be Concise:** Recommend only the necessary tests for the next step in diagnosis. Do not list every possible test. 

    **Output Format:**
    You MUST respond with a valid JSON object that strictly adheres to the following Pydantic models. Do not add any explanatory text outside of the JSON structure.
    """

    try:
        print("Requesting test recommendations from OpenAI...")
        response = client.chat.completions.parse(
            model="gpt-4o" if not use_ppio else "qwen/qwen3-235b-a22b-thinking-2507",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Here is the transcription:\n\n---\n{transcription}\n---",
                },
            ],
            response_format=TestRecommendations,  # Enforce JSON output
        )

        response_content = response.choices[0].message.content
        print("Received raw response from OpenAI.")

        # --- 3. Parsing and Validation with Pydantic ---
        # This ensures the AI's output matches our desired structure.
        parsed_json = json.loads(response_content)
        validated_recommendations = TestRecommendations.model_validate(parsed_json)

        print("Successfully parsed and validated the recommendations.")
        return validated_recommendations

    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from OpenAI response.")
        print("Raw response:", response_content)
        return None
    except ValidationError as e:
        print("Error: OpenAI response did not match the Pydantic model.")
        print(e)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# --- 4. Example Usage ---
if __name__ == "__main__":
    sample_transcription = """
    医生: "李女士，您好，请问您哪里不舒服？"
    患者: "医生，我...我从今天早上开始，胸口这里就特别疼，是那种压着的感觉，喘不过气来。"
    医生: "这种疼痛持续了多久？有没有向其他地方放射？比如肩膀或者后背？"
    患者: "大概有半个多小时了，感觉左边肩膀和胳膊都有点麻麻的疼。"
    医生: "好的。您以前有过类似的情况吗？有没有高血压或者糖尿病的病史？"
    患者: "没有，这是第一次。我有高血压，一直在吃降压药，但是最近工作忙，有时候会忘记吃。"
    医生: "明白了。我们得尽快做一些检查来确定原因。"
    """

    recommendations = get_test_recommendations(sample_transcription)

    if recommendations:
        print("\n--- Recommended Diagnostic Tests ---")
        for test in recommendations.recommendations:
            print(f"- Test Name: {test.test_name}")
            if test.notes:
                print(f"  Notes: {test.notes}")
        print("----------------------------------")
