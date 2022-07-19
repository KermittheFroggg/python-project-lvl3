import logging
import os
import sys
import requests
import re
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse
from progress.bar import Bar

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.WARNING)
stderr_handler.setFormatter(formatter)

file_handler = logging.FileHandler('loader.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stderr_handler)


def url_t_file_path(url):
    file_path = url.split('//')
    file_path = re.sub(r'[\W_]+', '-', file_path[1])
    return file_path


def diff_netloc(urlapass_url_netloc, urlapass_netloc, src):
    if urlapass_url_netloc == urlapass_netloc:
        resource_path, ending = os.path.splitext(src)
    else:
        resource_path, ending = None, None
    return resource_path, ending


def finding_scheme(src, url):
    urlapass = urlparse(src)
    urlapass_url = urlparse(url)
    if urlapass.scheme != '' and urlapass.netloc != '':
        resource_path, ending = \
            diff_netloc(urlapass_url.netloc, urlapass.netloc, src)
    elif urlapass.scheme == '' and urlapass.netloc == '':
        resource_path, ending = os.path.splitext(src)
        resource_path = urlapass_url.scheme + '://' + \
            urlapass_url.netloc + resource_path  
    elif urlapass.scheme == '' and urlapass.netloc != '':
        if urlapass_url.netloc == urlapass.netloc:
            resource_path, ending = os.path.splitext(src)
            resource_path = urlapass_url.scheme + ':' + resource_path
        else:
            resource_path, ending = None, None
    if ending == '':
        ending = '.html'
    return resource_path, ending


def download(url, path):
    file_path = os.path.join(path, url_t_file_path(url) + '.html')
    r = requests.get(url, allow_redirects=True)
    if r.status_code != 200:
        logger.warning("Problems with URL", exc_info=True)
        raise requests.ConnectionError
    with Bar(
        'Downloading html:',
        fill='░',
        max=3000,
        suffix='%(percent).1f%% %(eta)ds'
    ) as bar:
        for i in range(3000):
            page = r.text
            bar.next()
    if not os.path.exists(path):
        logger.warning('Try another directory', exc_info=True)
        raise FileNotFoundError
    else:
        with open(file_path, 'w') as fp:
            fp.write(page)
            download_resources(file_path, url, path)
        return file_path


def download_resources(file_path, url, path):
    with open(file_path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        all_img = soup.find_all('img')
        all_links = soup.find_all('link')
        all_scripts = soup.find_all('script')
        resources_path = url_t_file_path(url) + '_files'
        Path(os.path.join(path, resources_path)).mkdir(exist_ok=True)
        for img in all_img:
            img_new_path = download_img(img, url, resources_path, path)
            if img_new_path != '':
                img['src'] = img_new_path
        for link in all_links:
            link_new_path = download_link(link, url, resources_path, path)
            if link_new_path != '':
                link['href'] = link_new_path
        for script in all_scripts:
            script['src'] = download_script(script, url, resources_path, path)
    with open(file_path, 'w') as fp:
        fp.write(soup.prettify())


def download_content(src, url, resources_path, path):
    resource_path, ending = finding_scheme(src, url)
    if resource_path is not None and ending is not None:
        r = requests.get(resource_path + ending, allow_redirects=True)
        if r.status_code != 200:
            logger.warning("Problems with URL", exc_info=True)
            raise requests.ConnectionError
        with Bar(
            'Downloading content:',
            fill='⣿',
            max=20000,
            suffix='%(percent).1f%% %(eta)ds'
        ) as bar:
            for i in range(20000):
                content = r.content
                bar.next()
        res_path_url = (
            os.path.join(resources_path, url_t_file_path(resource_path))
        )
        plus_ending = res_path_url + ending
        resource_path2 = os.path.join(path, plus_ending)
        with open(resource_path2, 'wb') as fp:
            fp.write(content)
        new_content_path = os.path.join(plus_ending)
        return new_content_path
    else:
        return src


def download_img(img, url, resources_path, path):
    if img.has_attr('src'):
        src = img['src']
        new_image_path = \
            download_content(src, url, resources_path, path)
        return new_image_path


def download_link(link, url, resources_path, path):
    if link.has_attr('href'):
        src = link['href']
        new_link_path = \
            download_content(src, url, resources_path, path)
        return new_link_path


def download_script(script, url, resources_path, path):
    if script.has_attr('src'):
        src = script['src']
        new_script_path = \
            download_content(src, url, resources_path, path)
        return new_script_path
