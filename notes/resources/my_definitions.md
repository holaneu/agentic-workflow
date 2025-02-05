# My definitions

## AI output data structure

output = {
  "status": "call_api_of_type_openai_official: Success",
  "message": {
    "content": completion.choices[0].message.content,
    "role": completion.choices[0].message.role,
  },        
  "info": {
    "model": completion.model,
    "prompt_tokens": completion.usage.prompt_tokens,
    "completion_tokens": completion.usage.completion_tokens,
    "total_tokens": completion.usage.total_tokens
  }
}