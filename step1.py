import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ["ANTHROPIC_API_KEY"]

#client = anthropic.Anthropic(api_key=api_key)  # or anthropic.Anthropic() to read the env var directly
client = anthropic.Anthropic(api_key=api_key) # explicitly set itgit remote add origin https://github.com/z-david/claude_console.git

resp = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=500,
    messages=[{"role": "user", "content": "Say hello in one sentence."}],
)
print(resp.stop_reason)      # "end_turn"
print(resp.content[0].text)