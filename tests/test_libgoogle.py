import sys

from loguru import logger
from rich.pretty import pprint

from libgoogle import connect, set_debug

logger.remove()
logger.add(sys.stderr, level="TRACE")


def test_gcal() -> None:
    print()
    gcal = connect("calendar.readonly", "v3")
    calendars = gcal.calendarList().list().execute()
    for item in calendars["items"]:
        pprint(item)
        break


def test_scope_prefix_stripping() -> None:
    """Test that full URL scope is normalized to short form."""
    print()
    gcal = connect("https://www.googleapis.com/auth/calendar.readonly", "v3")
    calendars = gcal.calendarList().list().execute()
    assert "items" in calendars


def test_gdrive() -> None:
    print()
    gdrive = connect("drive", "v3")
    about = gdrive.about().get(fields="user").execute()
    pprint(about)


def test_gmail() -> None:
    print()
    gmail = connect("gmail.readonly", "v1")
    labels = gmail.users().labels().list(userId="me").execute()
    for item in labels["labels"]:
        pprint(item)
        break


def test_debug() -> None:
    print()
    set_debug(True)

    gcal = connect("calendar.readonly", "v3")
    calendars = gcal.calendarList().list().execute()
    for item in calendars["items"]:
        pprint(item)
        break

    gdrive = connect("drive", "v3")
    about = gdrive.about().get(fields="user").execute()
    pprint(about)

    gmail = connect("gmail.readonly", "v1")
    labels = gmail.users().labels().list(userId="me").execute()
    for item in labels["labels"]:
        pprint(item)
        break

    set_debug(False)
