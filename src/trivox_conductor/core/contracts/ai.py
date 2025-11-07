from __future__ import annotations

from typing import Any, Dict

from .base_contract import Adapter


class AIBrainAdapter(Adapter):
    """Produce 3 options (hook/caption/hashtags) and optional song candidates."""

    def generate_options(
        self, manifest_snippet: Dict[str, Any]
    ) -> Dict[str, Any]: ...
