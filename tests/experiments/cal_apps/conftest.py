import pytest
from unittest.mock import patch
from dspygen.experiments.cal_apps.eventkit_mocks import MockEventKit, MockEKReminder

@pytest.fixture(autouse=True)
def mock_eventkit():
    mock_ek = MockEventKit()
    MockEventKit.patch()
    with patch.dict('sys.modules', {'EventKit': mock_ek}):
        with patch('EventKit.EKReminder', MockEKReminder):
            yield mock_ek