import logging
import os
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from progress.bar import Bar

logger = logging.getLogger()


def download(url, path):
    html_file_path = os.path.join(path, url_t_file_path(url) + '.html')
    r = requests.get(url, allow_redirects=True)
    if r.status_code != 200:
        logger.info("Problems with URL", exc_info=True)
        raise requests.ConnectionError
    page = r.text
    if not os.path.exists(path):
        logger.info('Try another directory', exc_info=True)
        raise FileNotFoundError
    logger.info(f'requested url: {url}')
    logger.info(f'output path: {path}')
    logger.info(f'write html file: {html_file_path}')
    with open(html_file_path, 'w') as fp:
        fp.write(page)
    download_resources(html_file_path, url, path)
    return html_file_path


def url_t_file_path(url):
    file_path = url.split('//')
    file_path = re.sub(r'[\W_]+', '-', file_path[1])
    return file_path


def download_resources(html_file_path, url, path):
    with open(html_file_path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        all_img = soup.find_all('img')
        all_links = soup.find_all('link')
        all_scripts = soup.find_all('script')
        folder_with_resources = url_t_file_path(url) + '_files'
        if not os.path.exists(os.path.join(path, folder_with_resources)):
            os.mkdir(os.path.join(path, folder_with_resources))
        for_lint(all_img,
                 all_links,
                 all_scripts,
                 url,
                 folder_with_resources,
                 path)
    with open(html_file_path, 'w') as fp:
        fp.write(soup.prettify())


def for_lint(all_img, all_links, all_scripts, url, folder_with_resources, path):
    with Bar('Downloading:', fill='░') as bar:
        for img in all_img:
            new_value_for_img = \
                download_img(img, url, folder_with_resources, path)
            if new_value_for_img != '':
                img['src'] = new_value_for_img
            bar.next()
    with Bar('Downloading:', fill='░') as bar:
        for link in all_links:
            new_value_for_link = \
                download_link(link, url, folder_with_resources, path)
            if new_value_for_link != '':
                link['href'] = new_value_for_link
            bar.next()
    with Bar('Downloading:', fill='░') as bar:
        for script in all_scripts:
            new_value_for_script = \
                download_script(script, url, folder_with_resources, path)
            if new_value_for_script != '':
                script['src'] = new_value_for_script
            bar.next()


def download_img(img, url, folder_with_resources, path):
    if img.has_attr('src'):
        old_value_of_resource = img['src']
        new_value_of_resource = \
            download_content(old_value_of_resource,
                             url,
                             folder_with_resources,
                             path)
        return new_value_of_resource


def download_link(link, url, folder_with_resources, path):
    if link.has_attr('href'):
        old_value_of_resource = link['href']
        new_value_of_resource = \
            download_content(old_value_of_resource,
                             url,
                             folder_with_resources,
                             path)
        return new_value_of_resource


def download_script(script, url, folder_with_resources, path):
    if script.has_attr('src'):
        old_value_of_resource = script['src']
        new_value_of_resource = \
            download_content(old_value_of_resource,
                             url,
                             folder_with_resources,
                             path)
        return new_value_of_resource


def download_content(old_value_of_resource, url, folder_with_resources, path):
    url_without_ending, ending = finding_scheme(old_value_of_resource, url)

    if url_without_ending is not None and ending is not None:
        if ending != '.html':
            r = requests.get(url_without_ending + ending, allow_redirects=True)
        else:
            r = requests.get(url_without_ending, allow_redirects=True)
        if r.status_code != 200:
            logger.info("Problems with URL", exc_info=True)
            raise requests.ConnectionError
        content = r.content
        folder_and_name_of_resource = (
            os.path.join(folder_with_resources,
                         url_t_file_path(url_without_ending))
        )
        resource_path_without_path = folder_and_name_of_resource + ending
        full_resource_path = os.path.join(path, resource_path_without_path)
        with open(full_resource_path, 'wb') as fp:
            fp.write(content)
        new_value_of_resource = resource_path_without_path
        return new_value_of_resource
    else:
        return old_value_of_resource


def finding_scheme(old_value_of_resource, url):
    urlapass_old_value_of_resource = urlparse(old_value_of_resource)
    urlapass_url = urlparse(url)
    if urlapass_old_value_of_resource.scheme != '' \
            and urlapass_old_value_of_resource.netloc != '':
        url_without_ending, ending = \
            diff_netloc(
                urlapass_url.netloc, urlapass_old_value_of_resource.netloc,
                old_value_of_resource
            )
    elif urlapass_old_value_of_resource.scheme == '' and (
            urlapass_old_value_of_resource.netloc == ''):
        url_without_ending, ending = os.path.splitext(old_value_of_resource)
        url_without_ending = urlapass_url.scheme + '://' + \
            urlapass_url.netloc + url_without_ending
    elif urlapass_old_value_of_resource.scheme == '' and (
            urlapass_old_value_of_resource.netloc != ''):
        if urlapass_url.netloc == urlapass_old_value_of_resource.netloc:
            url_without_ending, ending = os.path.splitext(old_value_of_resource)
            url_without_ending = urlapass_url.scheme + ':' + url_without_ending
        else:
            url_without_ending, ending = None, None
    if ending == '':
        ending = '.html'
    return url_without_ending, ending


def diff_netloc(urlapass_url_netloc, urlapass_netloc, src):
    if urlapass_url_netloc == urlapass_netloc:
        url_without_ending, ending = os.path.splitext(src)
    else:
        url_without_ending, ending = None, None
    return url_without_ending, ending
