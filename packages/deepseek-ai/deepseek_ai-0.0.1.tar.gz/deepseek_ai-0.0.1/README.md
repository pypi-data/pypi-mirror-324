# 🚀 DeepSeekAI: easy use the deepseek model

## Install

* Install from source (Recommend)

```bash
cd deepseek_ai
pip install -e .
```
* Install from PyPI
```bash
pip install deepseek-ai
```

## Quick Start
* All the code can be found in the `examples`
* Set DeepSeek API key in environment if using DeepSeek models: `export DEEPSEEK_API_KEY="sk-...".`
*  Maybe you can try loading environment variables like this. Create a new `.env` file
```
DEEPSEEK_API_KEY="sk-..."
```
```python
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)
```
##### It works with the Langchain library

```python
from deepseek_ai import DeepSeekAI

client = DeepSeekAI(
    api_key="sk-...",
)

messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]

response = client.chat.completions.create(
    model="deepseek_ai-chat",
    messages=messages
)

print(response.choices[0].message.content)
```