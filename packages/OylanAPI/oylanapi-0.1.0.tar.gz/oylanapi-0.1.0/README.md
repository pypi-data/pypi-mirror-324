# OylanAPI

OylanAPI is a Python library for interacting with the Oylan Assistant API, available at [oylan.nu.edu.kz](https://oylan.nu.edu.kz/). Before using this library, you must register on the website and obtain an API key. The resources consumed by the library will be tied to your account.

## Features
- Create, list, retrieve, update (PUT/PATCH), or delete assistants.
- Create interactions (sending text prompts, file prompts, images, etc.).
- Upload DOCX files to update an assistant's context.
- Retrieve available models from the Oylan Assistant platform.

## Installation
Once the library is published, install it via pip:

```bash
pip install OylanAPI
```

## Usage
Here's how to use the library:

```python
from OylanAPI import Client

# Create a client with your API key
client = Client(api_key="your-api-key")

# 1) List all assistants
assistants = client.list_assistants()
print("Assistants:", assistants)

# 2) Create a new assistant
new_assistant = client.create_assistant(
    name="My Assistant",
    description="Sample description",
    temperature=0.7,
    max_tokens=512,
    model="Oylan",
    system_instructions="System instructions here",
    context="Base context here"
)
print("Created assistant:", new_assistant)

# 3) Create an interaction
interaction_response = client.create_interaction(
    assistant_id=new_assistant["id"],
    text_prompt="Hello, can you summarize the contents of this file?"
)
print("Interaction response:", interaction_response)

# 4) Upload a DOCX file
upload_result = client.upload_docx(
    assistant_id=new_assistant["id"],
    file_paths=["/path/to/document.docx"]
)
print("Upload result:", upload_result)
```

## Note
- You need to register at [oylan.nu.edu.kz](https://oylan.nu.edu.kz/) and generate an API key from the **For Developers** -> **Api Keys** tab.
- All resource usage is tied to your account, so use your key responsibly.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

