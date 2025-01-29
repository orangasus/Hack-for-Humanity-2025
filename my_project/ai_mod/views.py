import requests

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTAzOTA1YjctNTA2YS00ZTkwLTg1NWEtZDQ4Y2YwYTA2NDg2IiwidHlwZSI6ImFwaV90b2tlbiJ9.Znxp42SJ2jCAzGiMZzzjcrhvFSiZToNOCoUWjkX9rRs'
headers = {"Authorization": f"Bearer {API_KEY}"}
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
        # openai/text-moderation-007
        nsfw_score = result["google"]["nsfw_likelihood"]
    except Exception as e:
        return {"Passed": False, "Error": e}
    else:
        passed = nsfw_score < NSFW_SCORE_CUTOFF
        return {"Passed": passed, "NSFW Score": nsfw_score}
