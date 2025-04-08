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
    "id": "S7iUw9i1ue",
    "title": "Quick Notes",
    "description": "Database for storing quick notes, ideas, and snippets. Supports plain text, markdown, and code snippets with tagging and timestamped entries.",
    "created_at": "2025-03-05T11:40:07.130391+00:00",
    "updated_at": "2025-04-07T11:00:48.927316+00:00",
    "version": "1.0",
    "owner": "vlada",
    "tags": [
      "notes"
    ]
  },
  "collections": {
    "notes": [
      {
        "content": "888",
        "created_at": "2025-04-07T11:00:48.927316+00:00",
        "updated_at": "2025-04-07T11:00:48.927316+00:00",
        "id": "k8aaqjtIDP"
      },
      {
        "content": "aaa",
        "created_at": "2025-04-03T09:34:03.650976+00:00",
        "updated_at": "2025-04-03T09:34:03.650976+00:00",
        "id": "y2kCWqLTQG"
      },
      {
        "content": "bobisek",
        "created_at": "2025-03-21T16:12:33.745776+00:00",
        "updated_at": "2025-03-21T16:12:33.745776+00:00",
        "id": "LoKMP5Y1KG"
      }
    ]
  },
  "db_json_schema": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
      "db_info": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "title": {
            "type": "string"
          },
          "description": {
            "type": "string"
          },
          "created_at": {
            "type": "string",
            "format": "date-time"
          },
          "updated_at": {
            "type": "string",
            "format": "date-time"
          },
          "version": {
            "type": "string"
          },
          "owner": {
            "type": "string"
          },
          "tags": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        },
        "required": [
          "id",
          "title",
          "description",
          "updated_at"
        ]
      },
      "collections": {
        "type": "object",
        "properties": {
          "notes": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string"
                },
                "created_at": {
                  "type": "string",
                  "format": "date-time"
                },
                "updated_at": {
                  "type": "string",
                  "format": "date-time"
                },
                "content": {
                  "type": "string"
                }
              },
              "required": [
                "id",
                "updated_at",
                "created_at",
                "content"
              ]
            }
          }
        },
        "required": [
          "notes"
        ]
      }
    },
    "required": [
      "db_info",
      "collections"
    ]
  }
}
```
