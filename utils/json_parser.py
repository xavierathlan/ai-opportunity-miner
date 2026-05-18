import json


def extract_json(text):

    try:
        start = text.find("{")
        end = text.rfind("}") + 1

        json_text = text[start:end]

        return json.loads(json_text)

    except Exception:

        return {
            "idea": "Erro ao interpretar resposta",
            "score": 0,
            "reason": text,
            "saas": "N/A"
        }