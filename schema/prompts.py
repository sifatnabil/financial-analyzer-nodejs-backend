def individual_serial(prompt) -> dict:
    return {
        "id": str(prompt["_id"]),
        "text": str(prompt["text"])
    }

def list_serial(prompts) -> list:
    return [individual_serial(prompt) for prompt in prompts]