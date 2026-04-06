from typing import Any

from .agents import TOOLS as AGENTS_TOOLS
from .artifacts import TOOLS as ARTIFACTS_TOOLS
from .conversations import TOOLS as CONVERSATIONS_TOOLS
from .crm import TOOLS as CRM_TOOLS
from .datastores import TOOLS as DATASTORES_TOOLS

TOOLS_DEFINITION: dict[str, dict[str, Any]] = {
    **AGENTS_TOOLS,
    **CONVERSATIONS_TOOLS,
    **ARTIFACTS_TOOLS,
    **DATASTORES_TOOLS,
    **CRM_TOOLS,
}
