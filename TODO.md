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
- [ ] Fix broken prompt tool references: `onboard_new_user` references nonexistent `contacts_post_contacts`, `broadcast_campaign` references nonexistent `dispatches_post_dispatches`, `create_new_agent` references `agents_post_agents` instead of `create_agent`
- [ ] Add `delete_agent` tool (DELETE `/agents/{id}`)
- [ ] Add Contacts tools: `list_contacts`, `get_contact`, `create_contact`, `update_contact`, `delete_contact`
- [ ] Add Dispatches tools: `list_dispatches`, `get_dispatch`, `create_dispatch`, `update_dispatch`, `delete_dispatch`

## P1 - High (Major capability gaps)
- [ ] Add tool annotations: `title`, `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint` to all tools
- [ ] Implement Resources: `resources/list`, `resources/read` for agent configs, conversation history, datastore info
- [ ] Implement Completions: `completion/complete` for auto-suggest on agent IDs, model names, status enums
- [ ] Add structured content to tool results: return `structuredContent` alongside `TextContent`
- [ ] Add structured error responses: return `{"error": true, "status": N, "message": "..."}` instead of plain text
- [ ] Add `outputSchema` to tools for response validation

## P2 - Medium (Important but not blocking)
- [ ] Add WhatsApp/Z-API messaging tools: `zapi_list_instances`, `zapi_send_text`, `zapi_send_media`, `zapi_send_template`
- [ ] Add CRM Scenario CRUD: `create_crm_scenario`, `get_crm_scenario`, `update_crm_scenario`, `delete_crm_scenario`
- [ ] Add missing Conversation tools: `create_conversation`, `resolve_conversation`, `delete_conversation`, `request_human_intervention`
- [ ] Add missing Datasource tools: `update_datasource`, `delete_datasource`, `sync_datasource`, `get_datasource_status`
- [ ] Add Agent Blacklist tools: `list_blacklist`, `add_to_blacklist`, `remove_from_blacklist`
- [ ] Add CRM Conversation Logs tools: `list_crm_logs`, `get_crm_log`
- [ ] Add Agent webhook listing: `get_agent_webhooks` (GET `/agents/{id}/webhook`)
- [ ] Add more workflow prompts: datastore setup, CRM management, artifact catalog, conversation troubleshooting, Z-API messaging
- [ ] Implement MCP notifications: emit `tools/list_changed` when tools change

## P3 - Low (Nice to have)
- [ ] Add test coverage reporting with pytest-cov (target: 100%)
- [ ] Fix file upload resource leak in loader.py (use context manager)
- [ ] Add retry logic with exponential backoff for transient failures
- [ ] Add rate limit handling (429 detection and backoff)
- [ ] Add request validation against inputSchema before API call
- [ ] Add Image/Audio content support for artifact media
- [ ] Add Embedded Resources support in tool results
- [ ] Add MCP-level pagination (cursors for list operations)

## Ralph Loop
- [ ] Update Ralph Loop to auto-fetch docs.chatvolt.ai when no tasks remain
- [ ] Update README with Ralph Loop usage instructions
