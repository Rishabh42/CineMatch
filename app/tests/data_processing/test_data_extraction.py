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