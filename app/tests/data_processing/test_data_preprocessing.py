# pytest . --html-report=./report/report.html -v

import pytest
import json
from ...data_processing_scripts.fetch_movie_details import fetch_movies
from ...data_processing_scripts.filter_movie_details import filter_response, send_curl_request


@pytest.fixture()
def random_file():
    return "non_existent_file"

def test_fetch_movies():
    try:
        assert fetch_movies('dummy_data_test/movie_list.csv') == "OK"
    except Exception as exc:
        pytest.fail(f"Unexpected exception raised: {exc}")

def test_fetch_movies_neg(random_file):
    with pytest.raises(FileNotFoundError) as excinfo:
        fetch_movies(random_file)
    assert str(excinfo.value) == f"{random_file} file not found."

def test_filter_movies():
    # This will work on McGill's network.
    try:
        assert filter_response('dummy_data_test/final_cleaned_movie_list.csv') == "OK"
    except Exception as exc:
        pytest.fail(f"Unexpected exception raised: {exc}")
    

def test_filter_movies_neg(random_file):
    with pytest.raises(FileNotFoundError) as excinfo:
        filter_response(random_file)
    assert str(excinfo.value) == f"file not found"
    
def test_fetch_movies_empty():
    try:
        assert fetch_movies('empty_movie_list.csv') == "OK"
    except Exception as exc:
        pytest.fail(f"Unexpected exception raised: {exc}")
# Testing extract_history with incorrect date format
def test_extract_history_date_format():
    with pytest.raises(ValueError) as excinfo:
        extract_history("history_wrong_date_format.csv")
    assert "incorrect date format" in str(excinfo.value).lower()

def test_movie_curl():
    # This will work on McGill's network.
    try:
        response = send_curl_request("the+mask+1994")
        assert "adult" in response
        assert "genres" in response
        assert "runtime" in response
        assert "vote_average" in response
        assert "spoken_languages" in response
    except Exception as exc:
        pytest.fail(f"Unexpected exception raised: {exc}")

