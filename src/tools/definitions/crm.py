from typing import Dict, Any

TOOLS: Dict[str, Dict[str, Any]] = {
    "list_crm_scenarios": {
        "method": "GET",
        "path": "/crm/scenario",
        "description": "List all CRM Scenarios, optionally filtered by agentId.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string"}
            }
        }
    },
    "list_crm_steps": {
        "method": "GET",
        "path": "/crm/step",
        "description": "List CRM steps for a given scenario.",
        "input_schema": {
            "type": "object",
            "properties": {
                "scenarioId": {"type": "string"},
                "agentId": {"type": "string"}
            },
            "required": ["scenarioId"]
        }
    },
    "create_crm_step": {
        "method": "POST",
        "path": "/crm/step",
        "description": "Create a new CRM step in a scenario.",
        "input_schema": {
            "type": "object",
            "properties": {
                "scenarioId": {"type": "string"},
                "name": {"type": "string"},
                "agentId": {"type": "string"},
                "trigger": {"type": "string"},
                "prompt": {"type": "string"},
                "initialMessage": {"type": "string"},
                "autoNextStepId": {"type": "string"},
                "autoNextTime": {"type": "integer"},
                "defaultStatus": {"type": "string", "enum": ["RESOLVED", "UNRESOLVED", "HUMAN_REQUESTED", "null"]},
                "defaultPriority": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "null"]},
                "assigneeLogicType": {"type": "string", "enum": ["none", "clear", "single_user", "random_selected", "fair_distribution_selected"]},
                "selectedMembershipIdsForAssignee": {"type": "array", "items": {"type": "string"}},
                "isRequired": {"type": "boolean"},
                "autoNextTimeUnit": {"type": "string", "enum": ["m", "h", "d", "null"]},
                "defaultTags": {"type": "array", "items": {"type": "string"}},
                "defaultTagsToRemove": {"type": "array", "items": {"type": "string"}},
                "requestContact": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "boolean"},
                        "email": {"type": "boolean"},
                        "phone": {"type": "boolean"}
                    }
                },
                "isConversationRemovalStep": {"type": "boolean"},
                "zapiAgentId": {"type": "string"},
                "zapiPhoneNumber": {"type": "string"},
                "zapiMessage": {"type": "string"},
                "whatsappTemplateAgentId": {"type": "string"},
                "whatsappTemplateName": {"type": "string"},
                "whatsappTemplateLanguageCode": {"type": "string"},
                "whatsappTemplateText": {"type": "string"},
                "defaultAiControl": {"type": "boolean"},
                "webhookUrl": {"type": "string"},
                "webhookHeader": {"type": "object"}
            },
            "required": ["scenarioId", "name"]
        }
    },
    "update_crm_step": {
        "method": "PUT",
        "path": "/crm/step",
        "description": "Update an existing CRM step. IMPORTANT: ID must be passed in the body.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the step to update"},
                "name": {"type": "string"},
                "trigger": {"type": "string"},
                "prompt": {"type": "string"},
                "initialMessage": {"type": "string"},
                "autoNextStepId": {"type": "string"},
                "autoNextTime": {"type": "integer"},
                "defaultStatus": {"type": "string", "enum": ["RESOLVED", "UNRESOLVED", "HUMAN_REQUESTED", "null"]},
                "defaultPriority": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "null"]},
                "assigneeLogicType": {"type": "string", "enum": ["none", "clear", "single_user", "random_selected", "fair_distribution_selected"]},
                "selectedMembershipIdsForAssignee": {"type": "array", "items": {"type": "string"}},
                "isRequired": {"type": "boolean"},
                "autoNextTimeUnit": {"type": "string", "enum": ["m", "h", "d", "null"]},
                "defaultTags": {"type": "array", "items": {"type": "string"}},
                "defaultTagsToRemove": {"type": "array", "items": {"type": "string"}},
                "requestContact": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "boolean"},
                        "email": {"type": "boolean"},
                        "phone": {"type": "boolean"}
                    }
                },
                "isConversationRemovalStep": {"type": "boolean"},
                "zapiAgentId": {"type": "string"},
                "zapiPhoneNumber": {"type": "string"},
                "zapiMessage": {"type": "string"},
                "whatsappTemplateAgentId": {"type": "string"},
                "whatsappTemplateName": {"type": "string"},
                "whatsappTemplateLanguageCode": {"type": "string"},
                "whatsappTemplateText": {"type": "string"},
                "defaultAiControl": {"type": "boolean"},
                "webhookUrl": {"type": "string"},
                "webhookHeader": {"type": "object"}
            },
            "required": ["id", "name"]
        }
    },
    "delete_crm_step": {
        "method": "DELETE",
        "path": "/crm/step",
        "description": "Delete a CRM step. IMPORTANT: ID must be passed in the body.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the step to delete"}
            },
            "required": ["id"]
        }
    },
    "add_conversation_to_step": {
        "method": "POST",
        "path": "/crm/step/conversation",
        "description": "Add an existing conversation to a specific CRM step within a scenario.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation to add"},
                "scenarioId": {"type": "string", "description": "ID of the scenario (required if stepId is not provided)"},
                "stepId": {"type": "string", "description": "ID of the specific CRM step"},
                "stepIndex": {"type": "integer", "description": "Index of the step within the scenario"}
            },
            "required": ["conversationId"]
        }
    },
    "move_conversation_to_step": {
        "method": "POST",
        "path": "/crm/step/move",
        "description": "Move a conversation to another CRM step within a scenario.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation to move"},
                "scenarioId": {"type": "string", "description": "ID of the scenario"},
                "destStepId": {"type": "string", "description": "ID of the destination step"},
                "destStepIndex": {"type": "integer", "description": "Index of the destination step within the scenario"},
                "shouldSendInitialMessage": {"type": "boolean", "default": False}
            },
            "required": ["conversationId"]
        }
    }
}
