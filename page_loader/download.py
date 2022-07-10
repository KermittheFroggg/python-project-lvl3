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
    page = r.text
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


def download_content(resource_path, ending, resources_path, path):
    r = requests.get(resource_path + ending, allow_redirects=True)
    content = r.content
    res_path_url = (
        os.path.join(resources_path, url_t_file_path(resource_path))
    )
    plus_ending = res_path_url + ending
    resource_path2 = os.path.join(path, plus_ending)
    return resource_path2, plus_ending, content


def download_img(img, url, resources_path, path):
    if img.has_attr('src'):
        src = img['src']
        resource_path, ending = finding_scheme(src, url)
        if resource_path is not None and ending is not None:
            resource_path2, plus_ending, content = \
                download_content(resource_path, ending, resources_path, path)
            with open(resource_path2, 'wb') as fp:
                fp.write(content)
            new_image_path = os.path.join(plus_ending)
            return new_image_path
        else:
            return src


def download_link(link, url, resources_path, path):
    if link.has_attr('href'):
        src = link['href']
        resource_path, ending = finding_scheme(src, url)
        if resource_path is not None and ending is not None:
            resource_path2, plus_ending, content = \
                download_content(resource_path, ending, resources_path, path)
            with open(resource_path2, 'wb') as fp:
                fp.write(content)
            new_link_path = os.path.join(plus_ending)
            return new_link_path
        else:
            return src


def download_script(script, url, resources_path, path):
    if script.has_attr('src'):
        src = script['src']
        resource_path, ending = finding_scheme(src, url)
        if resource_path is not None and ending is not None:
            resource_path2, plus_ending, content = \
                download_content(resource_path, ending, resources_path, path)
            with open(resource_path2, 'wb') as fp:
                fp.write(content)
            new_script_path = os.path.join(plus_ending)
            return new_script_path
        else:
            return src
