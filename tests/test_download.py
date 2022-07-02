import os
import tempfile
from page_loader.download import download
from unittest.mock import Mock
import requests
import requests_mock

def test_downlad():
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_path = os.path.join(os.getcwd(), tmpdirname)
        result = download('https://ru.hexlet.io/courses', temp_path)
        assert result == os.path.join(temp_path, 'ru-hexlet-io-courses.html')

def test_for_each():
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_path = os.path.join(os.getcwd(), tmpdirname)
        url = 'https://ru.hexlet.io/courses'
        with requests_mock.Mocker() as m:
            m.get(url)
            download(url, temp_path)
        assert m.call_count == 1
