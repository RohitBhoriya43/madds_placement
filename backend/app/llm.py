import httpx, json, re
from .config import settings


class LLMClient:
    async def generate(self, system: str, prompt: str) -> str:
        if settings.llm_provider.lower() != "ollama":
            return ""

        url = f"{settings.ollama_base_url.rstrip('/')}/api/generate"

        payload = {
            "model": settings.ollama_model,
            "system": system,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.1,
            },
        }

        try:
            timeout = httpx.Timeout(
                connect=30.0,
                read=300.0,
                write=30.0,
                pool=30.0
            )


            async with httpx.AsyncClient(timeout=timeout) as client:

                response = await client.post(
                    url,
                    json=payload
                )

                response.raise_for_status()

                ollama_data = response.json()

                raw_response = ollama_data.get("response", "")

                print("RAW LLM RESPONSE:")
                print(raw_response)

                # return parse_llm_json(raw_response)
                if isinstance(raw_response, str):
                    raw_response = json.loads(raw_response)
                return raw_response

        except Exception as exc:

            print("LLM ERROR TYPE:", type(exc).__name__)
            print("LLM ERROR:", repr(exc))

            return {}

def parse_llm_json(response: str) -> dict:

    response = response.strip()

    if not response:
        raise ValueError("Empty response from LLM")

    # 1. Direct JSON
    try:
        data = json.loads(response)

        if isinstance(data, dict):
            return data

    except json.JSONDecodeError:
        pass

    # 2. JSON markdown block
    match = re.search(
        r"```json\s*(.*?)\s*```",
        response,
        re.DOTALL | re.IGNORECASE
    )

    if match:

        json_text = match.group(1).strip()

        try:
            data = json.loads(json_text)

            if isinstance(data, dict):
                return data

        except json.JSONDecodeError:
            pass

    # 3. Find JSON object
    start = response.find("{")
    end = response.rfind("}")

    if start != -1 and end != -1:

        json_text = response[start:end + 1]

        try:
            data = json.loads(json_text)

            if isinstance(data, dict):
                return data

        except json.JSONDecodeError as exc:

            print("JSON parsing failed:")
            print(exc)

            print("Extracted JSON:")
            print(json_text)

    raise ValueError(
        f"LLM did not return valid JSON:\n{response}"
    )


llm = LLMClient()