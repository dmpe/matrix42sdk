import os
import pytest
import requests
import sys
import urllib3
from typing import Optional


urllib3.disable_warnings()

# Simulate bash export


@pytest.fixture
def get_url() -> str:
    return os.environ.get("MATRIX42_URL").rstrip("/")


@pytest.fixture
def get_api_token() -> Optional[str]:
    return os.environ.get("MATRIX42SDK_API_TOKEN", None)
