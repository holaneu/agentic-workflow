# Custom Structured Outputs
Custom Structured Outputs allow you to ensure the model provides an answer in a very specific JSON format by supplying a clear JSON schema. This approach allows the model to consistently deliver responses with the correct typing and keywords.

The request is structured to ensure that the response adheres to the specified custom JSON schema. The schema defines the structure of a Book object with name and authors properties.

```curl
curl --location "https://api.mistral.ai/v1/chat/completions" \
     --header 'Content-Type: application/json' \
     --header 'Accept: application/json' \
     --header "Authorization: Bearer $MISTRAL_API_KEY" \
     --data '{
    "model": "ministral-8b-latest",
    "messages": [
     {
        "role": "system",
        "content": "Extract the books information."
      },
     {
        "role": "user",
        "content": "I recently read To Kill a Mockingbird by Harper Lee."
      }
    ],
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "schema": {
          "properties": {
            "name": {
              "title": "Name",
              "type": "string"
            },
            "authors": {
              "items": {
                "type": "string"
              },
              "title": "Authors",
              "type": "array"
            }
          },
          "required": ["name", "authors"],
          "title": "Book",
          "type": "object",
          "additionalProperties": false
        },
        "name": "book",
        "strict": true
      }
    },
    "max_tokens": 256,
    "temperature": 0
  }'
```

note
To better guide the model, the following is being always prepended by default to the System Prompt when using this method:

Your output should be an instance of a JSON object following this schema: {{ json_schema }}

However, it is recommended to add more explanations and iterate on your system prompt to better clarify the expected schema and behavior.

FAQ
Q: Which models support custom Structured Outputs?
A: All currently available models except for codestral-mamba are supported.