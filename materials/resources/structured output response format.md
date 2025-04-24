```python
response_format = {
  "type": "json",
  "schema": {
      "type": "object",
      "properties": {
          "cs": {"type": "string"},
          "en": {"type": "string"},
          "type": {"type": "string", "enum": ["phrase", "sentence"]}
      }
  }
}
```