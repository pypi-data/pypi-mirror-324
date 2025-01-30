{
    "name": "user_profile",
    "description": "represents a user.",
    "input_schema": {
        "properties": {
            "name": {
                "anyOf": [{"type": "string"}, {"type": "null"}],
                "default": None,
                "description": None,
            },
            "age": {
                "anyOf": [{"type": "integer"}, {"type": "null"}],
                "default": None,
                "description": None,
            },
            "recent_memories": {
                "description": None,
                "items": {"type": "string"},
                "type": "array",
            },
        },
        "required": ["recent_memories"],
        "type": "object",
    },
}

{
    "description": "represents a user.",
    "properties": {
        "name": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "default": None,
            "title": "Name",
        },
        "age": {
            "anyOf": [{"type": "integer"}, {"type": "null"}],
            "default": None,
            "title": "Age",
        },
        "recent_memories": {
            "items": {"type": "string"},
            "title": "Recent Memories",
            "type": "array",
        },
    },
    "required": ["recent_memories"],
    "title": "user_profile",
    "type": "object",
}
