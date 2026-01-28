from mcp import types

PROMPTS = {
    "onboard_new_user": types.Prompt(
        name="onboard_new_user",
        description="A guide to creating a contact and sending a welcome message.",
        arguments=[
            types.PromptArgument(
                name="first_name",
                description="Contact's first name",
                required=True
            ),
            types.PromptArgument(
                name="phone_number",
                description="Contact's phone number",
                required=True
            )
        ]
    ),
    "support_ticket_workflow": types.Prompt(
        name="support_ticket_workflow",
        description="Retrieve conversation history and create a CRM entry.",
        arguments=[
            types.PromptArgument(
                name="conversation_id",
                description="The ID of the conversation to summarize",
                required=True
            )
        ]
    ),
    "broadcast_campaign": types.Prompt(
        name="broadcast_campaign",
        description="Setup a dispatch for a list of contacts.",
        arguments=[
            types.PromptArgument(
                name="campaign_name",
                description="Name of the campaign",
                required=True
            )
        ]
    ),
    "create_new_agent": types.Prompt(
        name="create_new_agent",
        description="Interactive workflow to design, configure, and deploy a new AI agent.",
        arguments=[
            types.PromptArgument(
                name="agent_name",
                description="Desired name for the agent",
                required=False
            )
        ]
    )
}

def get_prompt_message(name: str, arguments: dict) -> types.GetPromptResult:
    if name == "onboard_new_user":
        first_name = arguments.get("first_name")
        phone = arguments.get("phone_number")
        return types.GetPromptResult(
            description="Onboarding Workflow",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"I want to onboard a new user named {first_name} with phone {phone}. "
                             f"Please first use the 'contacts_post_contacts' tool to create the contact, "
                             f"then ask me for a message template to send via 'whatsapp_post_zapi_instanceId_contactPhone_message'."
                    )
                )
            ]
        )
    elif name == "support_ticket_workflow":
        conv_id = arguments.get("conversation_id")
        return types.GetPromptResult(
            description="Support Ticket Workflow",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"I need to handle a support ticket for conversation {conv_id}. "
                             f"First, retrieve the messages using 'conversations_get_conversations_id_messages'. "
                             f"Then, summarize the issue and use 'crm_post_crm_entries' to log it."
                    )
                )
            ]
        )
    elif name == "broadcast_campaign":
        name = arguments.get("campaign_name")
        return types.GetPromptResult(
            description="Broadcast Campaign Workflow",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Let's set up the broadcast campaign '{name}'. "
                             f"I'll need to filter contacts first using 'contacts_get_contacts'. "
                             f"After I confirm the list, we will create a dispatch using 'dispatches_post_dispatches'."
                    )
                )
            ]
        )
    elif name == "create_new_agent":
        agent_name = arguments.get("agent_name", "a new agent")
        return types.GetPromptResult(
            description="Agent Creation Workflow",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"I want to create {agent_name}. Let's go through the steps:\n"
                             f"1. Help me define its role and goal (description).\n"
                             f"2. Help me draft a comprehensive system prompt.\n"
                             f"3. Ask me which LLM model to use (e.g., gpt-4o, claude-3-5-sonnet).\n"
                             f"4. Once we have the config, use 'agents_post_agents' to create it."
                    )
                )
            ]
        )
    else:
        raise ValueError(f"Unknown prompt: {name}")
