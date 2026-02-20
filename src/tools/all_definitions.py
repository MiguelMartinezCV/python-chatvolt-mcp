from typing import Dict, Any
from .definitions.agents import TOOLS as AGENTS_TOOLS
from .definitions.conversations import TOOLS as CONVERSATIONS_TOOLS
from .definitions.artifacts import TOOLS as ARTIFACTS_TOOLS
from .definitions.datastores import TOOLS as DATASTORES_TOOLS
from .definitions.crm import TOOLS as CRM_TOOLS

TOOLS_DEFINITION: Dict[str, Dict[str, Any]] = {
    **AGENTS_TOOLS,
    **CONVERSATIONS_TOOLS,
    **ARTIFACTS_TOOLS,
    **DATASTORES_TOOLS,
    **CRM_TOOLS
}