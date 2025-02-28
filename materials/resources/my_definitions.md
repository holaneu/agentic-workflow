# My definitions

## AI output data structure
Json format, example of python implementation:
```python
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
```

## Universal JSON dastabase structure
```json
{ 
  "db_info": {
    "id": "some_id",
    "title": "some title",
    "description": "some description",
    "created_at": "2025-02-26T12:00:00Z",
    "updated_at": "2025-02-26T12:00:00Z",
    "version": "1.0",
    "owner": "some owner id",
    "tags": ["tag1","tag2"],
    "last_modified_by": "some user modified the db"
  },
  "collections": {
    "users": [
      {
        "id": "user1",
        "name": "Jane Doe",
        "email": "jane@example.com"
      }
    ],
    "posts": [
      {
        "id": "post1",
        "authorId": "user1",
        "title": "My First Post",
        "content": "Hello, world!",
        "commentIds": ["comment1", "comment2"]
      }
    ],
    "comments": [
      {
        "id": "comment1",
        "postId": "post1",
        "author": "John Smith",
        "content": "Great post!"
      }
    ]
  }
}
```
