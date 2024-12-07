import pytest
from config_parser import parse_config
def test_parse_simple_constant():
    input_text = "PI is 3.14;\n"
    expected_output = ""
    assert parse_config(input_text) == expected_output

def test_parse_constant_evaluation():
    input_text = "PI is 3.14;\nEULER = [PI]\n"
    expected_output = "EULER = 3.14"
    assert parse_config(input_text) == expected_output

def test_parse_dictionary():
    input_text = '"settings" = @{ \n  color = "blue"; \n  size = "large"; \n}\n'
    expected_output = '\n[settings]\n\n    color = "blue"\n    size = "large"'
    assert parse_config(input_text) == expected_output

def test_parse_nested_dictionary():
    input_text = '"settings" = @{ \n  "display" = @{ \n    resolution = "1920x1080"; \n  };\n}\n'
    expected_output = '\n[settings]\n\n\n    [display]\n\n        resolution = "1920x1080"'
    assert parse_config(input_text) == expected_output

def test_parse_empty_input():
    input_text = ""
    expected_output = ""
    assert parse_config(input_text) == expected_output

def test_parse_comment_lines():
    input_text = "% This is a comment\nPI is 3.14;\n"
    expected_output = ""
    assert parse_config(input_text) == expected_output

if __name__ == "__main__":
    pytest.main()
