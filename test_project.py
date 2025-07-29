import pytest
from project import get_page, get_location, get_title, split_entries

def test_get_title():
    assert get_title("Los Buddenbrook (Thomas Mann)") == "Los Buddenbrook"

def test_get_location():
    assert get_location("- Your Highlight on page 65 | Location 983-985 | Added on Thursday, December 26, 2019 12:04:11 PM") == "983-985"

def test_get_page():
    assert get_page("- Your Highlight on page 114 | Location 1744-1746 | Added on Thursday, January 9, 2020 5:19:58 PM") == "114"

def test_split_entries():
    assert split_entries(["hola", "==========\n", "adiós", "==========\n"]) == [[1, "hola"], [2, "adiós"]]
