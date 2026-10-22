import anthropic, json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ["ANTHROPIC_API_KEY"]

client = anthropic.Anthropic(api_key=api_key)

tools = [{
    "name": "get_weather",
    "description": "Get the current weather for a city.",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
    },
}]

def run_tool(name, args):
    if name == "get_weather":
        return f"It's 18°C and cloudy in {args['city']}."  # fake data is fine
    return "Unknown tool"

messages = [{"role": "user", "content": "Compare the weather in Paris and Rome."}]

while True:
    resp = client.messages.create(
        model="claude-sonnet-5-5", max_tokens=1000,
        tools=tools, messages=messages,
    )

    # --- inspect the raw response structure ---
    print("stop_reason:", resp.stop_reason)
    print("raw_content:", resp)
    for b in resp.content:
        print(type(b).__name__, "->", b.model_dump())
    print("-" * 40)

    messages.append({"role": "assistant", "content": resp.content})

    if resp.stop_reason != "tool_use":
        break

    results = []
    for b in resp.content:
        if b.type == "tool_use":
            print("Claude called:", b.name, "with", b.input)
            results.append({
                "type": "tool_result",
                "tool_use_id": b.id,
                "content": run_tool(b.name, b.input),
            })

    messages.append({"role": "user", "content": results})

print(resp.content[0].text)