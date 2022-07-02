import os
import requests
import re


def download(url, path):
    file_path, _ = os.path.splitext(url)
    file_path = file_path.split('//')
    file_path = re.sub(r'[\W_]+', '-', file_path[1])
    file_path = path + '/' + file_path + '.html'
    r = requests.get(url, allow_redirects=True)
    page = r.text
    print(file_path)
    with open(file_path, 'w') as fp:
        fp.write(page)
    return file_path
