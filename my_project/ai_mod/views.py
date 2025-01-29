import requests
from dotenv import load_dotenv
import os

load_dotenv()
AI_API_KEY = os.getenv("AI_API_KEY")
print(AI_API_KEY)

headers = {"Authorization": f"Bearer {AI_API_KEY}"}
url = "https://api.edenai.run/v2/text/moderation"
payload = lambda txt: {
    "providers": "google",
    "language": "en",
    "text": txt,
}

NSFW_SCORE_CUTOFF = 4


def check_review_for_nsfw(title_n_text):
    """
    The range for NSFW score is 1-5 included
    """
    try:
        response = requests.post(url, json=payload(title_n_text), headers=headers)
        result = response.json()
        print(result)
        # openai/text-moderation-007
        nsfw_score = result["google"]["nsfw_likelihood"]
    except Exception as e:
        print({"Passed": False, "Error": e})
        return {"Passed": False, "Error": e}
    else:
        passed = nsfw_score < NSFW_SCORE_CUTOFF
        print({"Passed": passed, "NSFW Score": nsfw_score})
        return {"Passed": passed, "NSFW Score": nsfw_score}
