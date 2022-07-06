import os
import requests
import re
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse


def url_t_file_path(url):
    file_path = url.split('//')
    file_path = re.sub(r'[\W_]+', '-', file_path[1])
    return file_path


def finding_scheme(src, url):
    urlapass = urlparse(src)
    urlapass_url = urlparse(url)
    if urlapass.scheme != '' and urlapass.netloc != '':
        resource_path, ending = os.path.splitext(src)
    elif urlapass.scheme == '' and urlapass.netloc == '':
        resource_path, ending = os.path.splitext(src)
        resource_path = urlapass_url.scheme + '://' + \
            urlapass_url.netloc + resource_path
    elif urlapass.scheme == '' and urlapass.netloc != '':
        resource_path, ending = os.path.splitext(src)
        resource_path = urlapass_url.scheme + '://' + resource_path
    return resource_path, ending


def download(url, path):
    file_path = os.path.join(path, url_t_file_path(url) + '.html')
    r = requests.get(url, allow_redirects=True)
    page = r.text
    with open(file_path, 'w') as fp:
        fp.write(page)
        download_resources(file_path, url, path)
    return file_path


def download_resources(file_path, url, path):
    with open(file_path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        all_img = soup.find_all('img')
        resources_path = url_t_file_path(url) + '_files'
        Path(os.path.join(path, resources_path)).mkdir(exist_ok=True)
        for img in all_img:
            if img.has_attr('src'):
                src = img['src']
                resource_path, ending = finding_scheme(src, url)
                r = requests.get(resource_path + ending, allow_redirects=True)
                image = r.content
                res_path_url = (
                    os.path.join(resources_path, url_t_file_path(resource_path))
                )
                resource_path2 = os.path.join(path, res_path_url + ending)
                with open(resource_path2, 'wb') as fp:
                    fp.write(image)
                new_image_path = os.path.join(res_path_url + ending)
                img['src'] = new_image_path
    with open(file_path, 'w') as fp:
        fp.write(soup.prettify())
