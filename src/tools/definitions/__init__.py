from typing import Dict, Any
from .agents import TOOLS as AGENTS_TOOLS
from .conversations import TOOLS as CONVERSATIONS_TOOLS
from .artifacts import TOOLS as ARTIFACTS_TOOLS
from .datastores import TOOLS as DATASTORES_TOOLS
from .crm import TOOLS as CRM_TOOLS

TOOLS_DEFINITION: Dict[str, Dict[str, Any]] = {
    **AGENTS_TOOLS,
    **CONVERSATIONS_TOOLS,
    **ARTIFACTS_TOOLS,
    **DATASTORES_TOOLS,
    **CRM_TOOLS
}
