
from __future__ import annotations
from typing import Optional
import re

class SessionCorrelator:
    """
    Pure logic for mapping replay export files to session IDs.
    KISS: default rule looks for a 'session_id' token or uses a fallback naming template.
    """

    SESSION_RE = re.compile(r"session[_-](?P<sid>[A-Za-z0-9\-]+)", re.IGNORECASE)

    def correlate(self, filename: str, fallback_session: Optional[str] = None) -> Optional[str]:
        """
        Correlate a replay export filename to a session ID.
        
        :param filename: The replay export filename.
        :type filename: str
        
        :param fallback_session: Fallback session ID if none found in filename.
        :type fallback_session: Optional[str]
        
        :return: The correlated session ID or the fallback.
        :rtype: Optional[str]
        """
        m = self.SESSION_RE.search(filename)
        if m:
            return m.group("sid")
        return fallback_session
