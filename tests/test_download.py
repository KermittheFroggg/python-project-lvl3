import os
import shutil
import sys
import tempfile
from page_loader.download import download
import requests_mock
from page_loader.download import download_resources
import logging
import pytest
import pook
import requests


def logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    stdout_handler = logging.StreamHandler(sys.stderr)
    stdout_handler.setLevel(logging.WARNING)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('loader_test.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)
    logging.info('test started')

def test_downlad():
    logger()
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_path = os.path.join(os.getcwd(), tmpdirname)
        result = download('https://ru.hexlet.io/courses', temp_path)
        assert result == os.path.join(temp_path, 'ru-hexlet-io-courses.html')

def test_for_each():
    logger()
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_path = os.path.join(os.getcwd(), tmpdirname)
        url = 'https://ru.hexlet.io/courses'
        with requests_mock.Mocker() as m:
            m.get(url)
            download(url, temp_path)
        assert m.call_count == 1

def test_img():
    logger()
    pook.on()
    result_path = 'tests/fixtures/img_test_after.html'
    with tempfile.NamedTemporaryFile() as tmpfilename:
        shutil.copyfile('tests/fixtures/img_test_before.html', tmpfilename.name)
        url =  'https://ru.hexlet.io/courses'
        temp_path_file = tmpfilename.name
        dir,_  = os.path.split(tmpfilename.name)
        pook.get('https://ru.hexlet.io/assets/professions/nodejs.png', reply=200)
        download_resources(temp_path_file,  url, dir)
        with open(temp_path_file) as rslt:
            with open(result_path) as result:
                assert rslt.read() == result.read()


def test_img_files():
    logger()
    pook.on()
    with tempfile.NamedTemporaryFile() as tmpfilename:
        shutil.copyfile('tests/fixtures/img_test_before.html', tmpfilename.name)
        url =  'https://ru.hexlet.io/courses'
        temp_path_file = tmpfilename.name
        dir,_  = os.path.split(tmpfilename.name)
        pook.get('https://ru.hexlet.io/assets/professions/nodejs.png', reply=200)
        download_resources(temp_path_file,  url, dir)
        results = []
        for _,_,filenames in os.walk(dir):
            for file in filenames:
                fileExt=os.path.splitext(file)[-1]
                if fileExt == '.png' or fileExt == '.svg' or fileExt == '.jpg':
                    results.append(file)
        assert results != []


def test_link_script():
    logger()
    pook.on()
    result_path = 'tests/fixtures/link_script_after.html'
    with tempfile.NamedTemporaryFile() as tmpfilename:
        shutil.copyfile('tests/fixtures/link_script_before.html', tmpfilename.name)
        url =  'https://ru.hexlet.io/courses'
        temp_path_file = tmpfilename.name
        dir,_  = os.path.split(tmpfilename.name)
        pook.get('https://ru.hexlet.io/assets/professions/nodejs.png', reply=200)
        pook.get('https://ru.hexlet.io/assets/application.css', reply=200)
        pook.get('https://ru.hexlet.io/packs/js/runtime.js', reply=200)
        pook.get('https://ru.hexlet.io/courses.html', reply=200)
        download_resources(temp_path_file,  url, dir)
        with open(temp_path_file) as rslt:
            with open(result_path) as result:
                assert rslt.read() == result.read()


def test_link_script_files():
    logger()
    pook.on()
    with tempfile.NamedTemporaryFile() as tmpfilename:
        shutil.copyfile('tests/fixtures/link_script_before.html', tmpfilename.name)
        url =  'https://ru.hexlet.io/courses'
        temp_path_file = tmpfilename.name
        dir,_  = os.path.split(tmpfilename.name)
        pook.get('https://ru.hexlet.io/assets/professions/nodejs.png', reply=200)
        pook.get('https://ru.hexlet.io/assets/application.css', reply=200)
        pook.get('https://ru.hexlet.io/packs/js/runtime.js', reply=200)
        pook.get('https://ru.hexlet.io/courses.html', reply=200)
        download_resources(temp_path_file,  url, dir)
        results = []
        for _,_,filenames in os.walk(dir):
            for file in filenames:
                fileExt=os.path.splitext(file)[-1]
                if fileExt == '.css':
                    results.append(file)
        assert results != []


def test_errors():
    logger()
    pook.on()
    with tempfile.NamedTemporaryFile() as tmpfilename:
        dir,_  = os.path.split(tmpfilename.name)
        with pytest.raises(requests.exceptions.RequestException) as e:
            pook.get('https://ru.hexlet.io/assets/professions/nodejs.png', reply=200)
            pook.get('https://ru.hexlet.io/assets/application.css', reply=200)
            pook.get('https://ru.hexlet.io/packs/js/runtime.js', reply=200)
            pook.get('https://ru.hexlet.io/courses.html', reply=200)
            pook.get('https://ru.hexlet.io/courses', reply=400)
            download('https://ru.hexlet.io/courses', dir)
        assert e is not None


def test_hexlet_1():
    logger()
    pook.on()
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url =  'http://localhost/blog/about'
    file_name = 'localhost-blog-about.html'
    dir= os.path.join(os.getcwd(), temp_dir.name)
    temp_path_file = os.path.join(dir, file_name)
    shutil.copyfile('/home/frog/python-project-lvl3/tests/fixtures/localhost-blog-about.html', temp_path_file)
    pook.get('http://localhost/blog/about/assets/styles.css', reply=200)
    pook.get('http://localhost/photos/me.jpg', reply=200)
    pook.get('http://localhost/assets/scripts.js', reply=200)
    pook.get('http://localhost/blog/about.html', reply=200)
    download_resources(temp_path_file,  url, dir)
    ASSETS_DIR_NAME = 'localhost-blog-about_files'
    assert len(os.listdir(dir)) == 2
    assert len(os.listdir(os.path.join(dir, ASSETS_DIR_NAME))) == 4

def test_hexlet_1_2():
    logger()
    pook.on()
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url =  'https://site.com/blog/about'
    file_name = 'site-com-blog-about.html'
    dir= os.path.join(os.getcwd(), temp_dir.name)
    temp_path_file = os.path.join(dir, file_name)
    shutil.copyfile('/home/frog/python-project-lvl3/tests/fixtures/site-com-blog-about.html', temp_path_file)
    pook.get('https://site.com/blog/about/assets/styles.css', reply=200)
    pook.get('https://site.com/photos/me.jpg', reply=200)
    pook.get('https://site.com/assets/scripts.js', reply=200)
    pook.get('https://site.com/blog/about.html', reply=200)
    download_resources(temp_path_file,  url, dir)
    ASSETS_DIR_NAME = 'site-com-blog-about_files'
    assert len(os.listdir(dir)) == 2
    assert len(os.listdir(os.path.join(dir, ASSETS_DIR_NAME))) == 4


def test_hexlet_2():
    logger()
    pook.on()
    result_path = '/home/frog/python-project-lvl3/tests/fixtures/expected/site-com-blog-about.html'
    with tempfile.NamedTemporaryFile() as tmpfilename:
        shutil.copyfile('/home/frog/python-project-lvl3/tests/fixtures/site-com-blog-about.html', tmpfilename.name)
        url =  'https://site.com/blog/about'
        temp_path_file = tmpfilename.name
        dir,_  = os.path.split(tmpfilename.name)
        pook.get('https://site.com/blog/about/assets/styles.css', reply=200)
        pook.get('https://site.com/photos/me.jpg', reply=200)
        pook.get('https://site.com/assets/scripts.js', reply=200)
        pook.get('https://site.com/blog/about.html', reply=200)
        download_resources(temp_path_file,  url, dir)
        with open(temp_path_file) as rslt:
            with open(result_path) as result:
                assert rslt.read() == result.read()
