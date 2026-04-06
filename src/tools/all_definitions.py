from typing import Any

from .definitions.agents import TOOLS as AGENTS_TOOLS
from .definitions.artifacts import TOOLS as ARTIFACTS_TOOLS
from .definitions.blacklist import TOOLS as BLACKLIST_TOOLS
from .definitions.contacts import TOOLS as CONTACTS_TOOLS
from .definitions.conversations import TOOLS as CONVERSATIONS_TOOLS
from .definitions.crm import TOOLS as CRM_TOOLS
from .definitions.datastores import TOOLS as DATASTORES_TOOLS
from .definitions.dispatches import TOOLS as DISPATCHES_TOOLS

TOOLS_DEFINITION: dict[str, dict[str, Any]] = {
    **AGENTS_TOOLS,
    **CONVERSATIONS_TOOLS,
    **ARTIFACTS_TOOLS,
    **DATASTORES_TOOLS,
    **CRM_TOOLS,
    **CONTACTS_TOOLS,
    **DISPATCHES_TOOLS,
    **BLACKLIST_TOOLS,
}
