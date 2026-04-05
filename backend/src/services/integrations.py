from __future__ import annotations

from datetime import datetime
from urllib.parse import quote_plus


def teams_meeting_url(title: str, start: datetime, end: datetime) -> str:
    return (
        "https://teams.microsoft.com/l/meeting/new"
        f"?subject={quote_plus(title)}"
        f"&startTime={quote_plus(start.isoformat())}"
        f"&endTime={quote_plus(end.isoformat())}"
    )


def outlook_event_url(title: str, start: datetime, end: datetime, location: str) -> str:
    return (
        "https://outlook.office.com/calendar/0/deeplink/compose"
        "?path=/calendar/action/compose"
        f"&subject={quote_plus(title)}"
        f"&startdt={quote_plus(start.isoformat())}"
        f"&enddt={quote_plus(end.isoformat())}"
        f"&location={quote_plus(location)}"
    )
