from typing import Any

from .agents import TOOLS as AGENTS_TOOLS
from .artifacts import TOOLS as ARTIFACTS_TOOLS
from .blacklist import TOOLS as BLACKLIST_TOOLS
from .contacts import TOOLS as CONTACTS_TOOLS
from .conversation_mgmt import TOOLS as CONVERSATION_MGMT_TOOLS
from .conversations import TOOLS as CONVERSATIONS_TOOLS
from .crm import TOOLS as CRM_TOOLS
from .crm_logs import TOOLS as CRM_LOGS_TOOLS
from .crm_scenarios import TOOLS as CRM_SCENARIOS_TOOLS
from .datasources import TOOLS as DATASOURCES_TOOLS
from .datastores import TOOLS as DATASTORES_TOOLS
from .dispatches import TOOLS as DISPATCHES_TOOLS
from .zapi import TOOLS as ZAPI_TOOLS

TOOLS_DEFINITION: dict[str, dict[str, Any]] = {
    **AGENTS_TOOLS,
    **CONVERSATIONS_TOOLS,
    **ARTIFACTS_TOOLS,
    **DATASTORES_TOOLS,
    **CRM_TOOLS,
    **CONTACTS_TOOLS,
    **DISPATCHES_TOOLS,
    **BLACKLIST_TOOLS,
    **CONVERSATION_MGMT_TOOLS,
    **CRM_SCENARIOS_TOOLS,
    **CRM_LOGS_TOOLS,
    **DATASOURCES_TOOLS,
    **ZAPI_TOOLS,
}
