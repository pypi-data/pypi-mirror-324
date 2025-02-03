import pytest
from dc_etexter.etexter import send_text

def test_send_text():
    """Test the send_text function."""
    smileyface = "\U0001F600"
    try:
        message = "You can send notifications from Python programs." + smileyface
        send_text(body=message)
    except Exception as e:
        pytest.fail(f"send_text() raised an exception: {e}")
