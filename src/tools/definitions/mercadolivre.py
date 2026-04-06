from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "mercadolivre_get_products": {
        "method": "GET",
        "path": "/mercadolivre/get-products",
        "description": "Retrieve a list of products from Mercado Livre with optional fuzzy search filtering.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "The ID of the agent"},
                "query": {"type": "string", "description": "The search query for fuzzy search"},
                "threshold": {"type": "number", "description": "The threshold for fuzzy search (default: 0.3)"},
                "maxResults": {"type": "integer", "description": "Maximum number of results to return"},
                "caseSensitive": {
                    "type": "boolean",
                    "description": "Whether search should be case-sensitive (default: false)",
                },
                "sortByRelevance": {"type": "boolean", "description": "Sort results by relevance (default: true)"},
                "partialMatch": {"type": "boolean", "description": "Allow partial matches (default: true)"},
                "typoTolerance": {"type": "integer", "description": "Typo tolerance for fuzzy search (default: 1)"},
            },
            "required": ["agentId"],
        },
    },
}
