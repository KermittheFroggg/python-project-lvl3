import os
import shutil
import tempfile
from page_loader.download import download
import requests_mock
from page_loader.download import download_resources
import logging

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

def test_img():
    result_path = 'tests/fixtures/img_test_after.html'
    with tempfile.NamedTemporaryFile() as tmpfilename:
        shutil.copyfile('tests/fixtures/img_test_before.html', tmpfilename.name)
        url =  'https://ru.hexlet.io/courses'
        temp_path_file = tmpfilename.name
        dir,_  = os.path.split(tmpfilename.name)
        download_resources(temp_path_file,  url, dir)
        with open(temp_path_file) as rslt:
            with open(result_path) as result:
                assert rslt.read() == result.read()


def test_img_files():
    with tempfile.NamedTemporaryFile() as tmpfilename:
        shutil.copyfile('tests/fixtures/img_test_before.html', tmpfilename.name)
        url =  'https://ru.hexlet.io/courses'
        temp_path_file = tmpfilename.name
        dir,_  = os.path.split(tmpfilename.name)
        download_resources(temp_path_file,  url, dir)
        results = []
        for _,_,filenames in os.walk(dir):
            for file in filenames:
                fileExt=os.path.splitext(file)[-1]
                if fileExt == '.png' or fileExt == '.svg' or fileExt == '.jpg':
                    results.append(file)
        assert results != []


def test_link_script():
    result_path = 'tests/fixtures/link_script_after.html'
    with tempfile.NamedTemporaryFile() as tmpfilename:
        shutil.copyfile('tests/fixtures/link_script_before.html', tmpfilename.name)
        url =  'https://ru.hexlet.io/courses'
        temp_path_file = tmpfilename.name
        dir,_  = os.path.split(tmpfilename.name)
        download_resources(temp_path_file,  url, dir)
        with open(temp_path_file) as rslt:
            with open(result_path) as result:
                assert rslt.read() == result.read()

def test_link_script_files():
    with tempfile.NamedTemporaryFile() as tmpfilename:
        shutil.copyfile('tests/fixtures/link_script_before.html', tmpfilename.name)
        url =  'https://ru.hexlet.io/courses'
        temp_path_file = tmpfilename.name
        dir,_  = os.path.split(tmpfilename.name)
        download_resources(temp_path_file,  url, dir)
        results = []
        for _,_,filenames in os.walk(dir):
            for file in filenames:
                fileExt=os.path.splitext(file)[-1]
                if fileExt == '.css':
                    results.append(file)
        assert results != []