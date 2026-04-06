# TODO - Chatvolt MCP Improvement Plan

<!--
Track tasks for the Ralph Loop. Check off items as they are completed.
The agent should work through unchecked items in order.
Priority: P0 (Critical) → P1 (High) → P2 (Medium) → P3 (Low)
-->

## P0 - Critical (Fix broken functionality)
- [x] Set up ruff linter and formatter
- [x] Configure ruff rules (E, F, I, W, UP, B, SIM)
- [x] Ensure all files pass ruff check
- [x] Ensure all files pass ruff format
- [x] Set up pytest with asyncio support
- [x] Ensure all existing tests pass
- [x] Fix broken prompt tool references
- [x] Add `delete_agent` tool
- [x] Add Contacts tools
- [x] Add Dispatches tools

## P1 - High (Major capability gaps)
- [x] Add tool annotations: title, readOnlyHint, destructiveHint, idempotentHint, openWorldHint
- [x] Implement Resources: chatvolt://models, chatvolt://tools, chatvolt://prompts, chatvolt://agent/{id} template
- [x] Implement Completions: auto-suggest for modelName, status, channel, type, method, priority
- [x] Add structured content to tool results
- [x] Add structured error responses
- [x] Add more resource templates: conversation, contact, dispatch, datastore
- [x] Add more completion values: visibility, direction, messageType, toolType

## P2 - Medium (Important but not blocking)
- [x] Add WhatsApp/Z-API messaging tools: zapi_list_instances, zapi_send_text/media/template/list/buttons
- [x] Add CRM Scenario CRUD tools
- [x] Add missing Conversation tools: create, resolve, delete, request_human_intervention
- [x] Add missing Datasource tools: update, delete, sync, get_datasource_status
- [x] Add Agent Blacklist tools
- [x] Add CRM Conversation Logs tools
- [x] Add more workflow prompts (8 total: onboard, broadcast, create_agent, setup_datastore, create_crm_workflow, whatsapp_outreach, contact_enrichment, agent_health_check)

## P3 - Low (Nice to have)
- [x] Add test coverage reporting with pytest-cov (target: 100%)
- [x] Add retry logic with exponential backoff for transient failures
- [x] Add rate limit handling (429 detection and backoff)
- [x] Add request validation against inputSchema before API call
- [x] Add Image/Audio content support for artifact media
- [x] Add MCP-level pagination (cursors for list operations)
- [x] Update README with complete documentation
- [x] Add async retry logic with exponential backoff for transient failures

## Ralph Loop
- [x] Update Ralph Loop to auto-fetch docs when idle
- [x] Update README with Ralph Loop usage instructions

## Stats
- **116 tools** implemented (agents, conversations, artifacts, datastores, CRM, contacts, dispatches, blacklist, Z-API, datasource management, WhatsApp Official, Interactive Messages, Twilio, Mercado Livre, Zapper, Contact Lists)
- **8 workflow prompts** implemented
- **67 tests** passing (76% coverage)
- **All tools have annotations** (title, readOnlyHint, destructiveHint, idempotentHint, openWorldHint)
- **Resources**: models, tools, prompts, agent/conversation/contact/dispatch/datastore templates
- **Completions**: modelName, status, channel, type, method, priority, visibility, direction, messageType, toolType, dispatchStatus, presencePenalty, frequencyPenalty, topP, temperature
- **Structured errors**: {error, status, message}
- **Pagination**: cursor-based pagination support for list operations (list_conversations, list_artifacts, list_contacts, list_dispatches, list_blacklist, list_crm_logs, list_crm_scenarios, list_crm_steps, list_datastores, list_datasources, list_artifact_media, list_contact_lists)
- **Async retries**: async retry logic with exponential backoff for transient failures
- **New integrations**: WhatsApp Official API (template messages, templates), Interactive Messages (buttons, list, CTA, location, contact), Twilio SMS, Mercado Livre products, Zapper messaging
- **Logging**: MCP logging capability with setLevel handler for client-configurable verbosity
- **Server metadata**: Added version, instructions to Server initialization
- **Tools listChanged**: Enabled tools.listChanged capability for real-time tool update notifications
- **Enhanced agent tools**: create_agent and update_agent now support visibility, handle, interfaceConfig, inactiveHours, external URL configs
- **New dispatch features**: populate_dispatch_queue, Contact List CRUD operations (list_contact_lists, get_contact_list, create_contact_list, update_contact_list, delete_contact_list)
