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


## 1. JSON Schema Definition

Using a JSON Schema, you can enforce rules and validate the structure of your database file. Below is an example schema for your universal JSON structure:

### JSON code
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Universal Database Schema",
  "type": "object",
  "required": ["db_info", "collections"],
  "properties": {
    "db_info": {
      "type": "object",
      "required": ["id", "title", "description", "created_at", "updated_at", "version", "owner"],
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
        }
      }
    },
    "collections": {
      "type": "object",
      "properties": {
        "users": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "name", "email"],
            "properties": {
              "id": { "type": "string" },
              "name": { "type": "string" },
              "email": { "type": "string", "format": "email" }
            }
          }
        },
        "posts": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "authorId", "title", "content"],
            "properties": {
              "id": { "type": "string" },
              "authorId": { "type": "string" },
              "title": { "type": "string" },
              "content": { "type": "string" },
              "commentIds": {
                "type": "array",
                "items": { "type": "string" }
              }
            }
          }
        },
        "comments": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "postId", "author", "content"],
            "properties": {
              "id": { "type": "string" },
              "postId": { "type": "string" },
              "author": { "type": "string" },
              "content": { "type": "string" }
            }
          }
        }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

### Key Points:
- **`$schema`**: Specifies the version of JSON Schema.
- **`required`**: Ensures that all necessary keys are present.
- **Format Validations**: For instance, `created_at` and `updated_at` must follow the `date-time` format.
- **`additionalProperties`:** Prevents the inclusion of keys not defined in the schema, which can be useful for ensuring strict structure.


## Validation against JSON schema
Below is an example of how you might validate a new "posts" record against your monolithic JSON schema (assumed to be stored in a file called `db_schema.json`). In this example, we extract the schema for an individual post (under `collections.posts.items`) and use the [jsonschema](https://pypi.org/project/jsonschema/) library to perform the validation.

### Python code
```python
import json
import jsonschema
from jsonschema import validate, ValidationError

def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def validate_post_record(post_record, db_schema):
    # Extract the "posts" record schema from the monolithic db_schema.json
    try:
        posts_schema = db_schema["properties"]["collections"]["properties"]["posts"]["items"]
    except KeyError as e:
        print("Error extracting posts schema:", e)
        return False

    try:
        validate(instance=post_record, schema=posts_schema)
        print("Post record is valid.")
        return True
    except ValidationError as ve:
        print("Validation error:", ve.message)
        return False

if __name__ == "__main__":
    # Load the monolithic JSON schema (db_schema.json)
    db_schema = load_json_file("db_schema.json")
    
    # Example new post record to be added to blog.json under collections.posts
    new_post = {
        "id": "post1",
        "authorId": "user1",
        "title": "My First Post",
        "content": "Hello, world!",
        "commentIds": ["comment1", "comment2"]
    }
    
    # Validate the new post record
    is_valid = validate_post_record(new_post, db_schema)
```

### How It Works

1. **Loading Files:**  
   The `load_json_file` function reads a JSON file from disk. In this case, it’s used to load your monolithic schema file (`db_schema.json`).

2. **Extracting the Posts Schema:**  
   In `validate_post_record`, we navigate through the JSON schema to get the schema for a single post:
   - The posts collection is defined under `"collections" → "posts"`, and we assume that the schema for each post is defined in the `"items"` property.

3. **Validation:**  
   The `validate` function from the jsonschema library checks the `post_record` against the extracted `posts_schema`. If the record is valid, it prints a success message; otherwise, it catches a `ValidationError` and prints the error message.

This example can be integrated into your Flask backend so that any time a new post record is submitted, it is validated against your schema before being added to the `blog.json` file.