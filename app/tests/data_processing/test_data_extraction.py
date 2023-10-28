# pytest test_data_extraction.py --html-report=./report/report.html

import pytest
from ...data_processing_scripts.process_rating import extract_ratings
from ...data_processing_scripts.process_history import extract_history

def test_extract_history():
    try:
        assert extract_history("dummy_data_test/history1.csv") == "SUCCESS"
    except Exception as exc:
        pytest.fail(f"Unexpected exception raised: {exc}")

def test_extract_ratings():
    try:
        assert extract_ratings("dummy_data_test/ratings.csv") == "SUCCESS"
    except Exception as exc:
        pytest.fail(f"Unexpected exception raised: {exc}")
# Testing extract_history with incorrect date format
def test_extract_history_date_format():
    with pytest.raises(ValueError) as excinfo:
        extract_history("dummy_data_test/history_wrong_date_format.csv")
    assert "incorrect date format" in str(excinfo.value).lower()
def test_extract_history_empty():
    try:
        assert extract_history('dummy_data_test/empty_history.csv') == "SUCCESS"
    except Exception as exc:
        pytest.fail(f"Unexpected exception raised: {exc}")