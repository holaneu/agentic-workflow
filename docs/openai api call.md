You can use Python's `requests` module to interact with the OpenAI API without relying on the `openai` Python package. Below is an example of how to achieve this using the `requests` module.

### Example Script

```python
import requests
import json

# Replace with your API key
api_key = "your_openai_api_key"

# Define the endpoint
url = "https://api.openai.com/v1/chat/completions"

# Define the headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Define the payload
payload = {
    "model": "gpt-3.5-turbo",  # Specify the model you want to use
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! How can I use OpenAI API with just requests module?"}
    ],
    "temperature": 0.7
}

# Send the request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Check the response
if response.status_code == 200:
    result = response.json()
    print(result["choices"][0]["message"]["content"])
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

### Explanation

1. **API Key**: Replace `"your_openai_api_key"` with your actual API key.
2. **Headers**: The `Authorization` header contains your Bearer token, and `Content-Type` specifies JSON.
3. **Payload**: Define the model and conversation context in the `messages` field.
   - `role`: Either `system`, `user`, or `assistant`.
   - `content`: The actual message content.
4. **Request**: Use `requests.post()` to send the payload to the OpenAI API endpoint.
5. **Response Handling**: If the request succeeds, the response will include the assistant's reply.

### Pros of Using `requests`
- No dependency on external SDKs.
- Fine-grained control over the request and response handling.

### Notes
- Make sure to handle errors (e.g., invalid API key, rate limits) appropriately in production code.
- Refer to the [OpenAI API documentation](https://platform.openai.com/docs/) for detailed usage and advanced options.