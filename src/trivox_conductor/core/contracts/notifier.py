from __future__ import annotations
from typing import Dict
from .base_contract import Adapter

class NotifierAdapter(Adapter):
    """Send a notification payload (Slack/Discord)."""
    def notify(self, payload: Dict) -> None: ...
