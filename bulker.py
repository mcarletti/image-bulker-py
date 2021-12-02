import requests
import mimetypes
import re
import os


class ImageBulker():
    def __init__(self, engine="google"):
        self.engine = engine

    def get_thumbnail_urls(self, keyword, size=1):
        if self.engine == "google":
            return self._get_thumbnail_urls_from_google(keyword, size)
        elif self.engine == "duckduckgo":
            return self._get_thumbnail_urls_from_duckduckgo(keyword, size)
        else:
            raise NotImplementedError()

    def _get_thumbnail_urls_from_google(self, keyword, size=1):

        imgs_per_page = 20
        image_search = 'http://images.google.com/images?q={}&start={}&sout=1&tbm=isch'
        extract_regex = r'\" src=\"(.*?)\"'

        offset = imgs_per_page * int(size / imgs_per_page)
        thumbnail_urls = []
        while offset >= 0:
            base_url = image_search.format(keyword, offset)
            html = requests.get(base_url).content
            urls = re.findall(extract_regex, str(html))
            thumbnail_urls += urls
            offset -= imgs_per_page
        thumbnail_urls = list(set(thumbnail_urls))
        return thumbnail_urls[:size]

    def _get_thumbnail_urls_from_duckduckgo(self, keyword, size=1):

        image_search = "https://duckduckgo.com/?q={}&atb=v226-1&iar=images&iax=images&ia=images"
        extract_regex = ""

        base_url = image_search.format(keyword)
        html = requests.get(base_url).content

        import pdb; pdb.set_trace()

        thumbnail_urls = []
        while len(thumbnail_urls) < size:
            urls = re.findall(extract_regex, str(html))
            thumbnail_urls += urls
            offset -= self.__imgs_per_page
        thumbnail_urls = list(set(thumbnail_urls))
        return thumbnail_urls[:size]

    def get_data_from_url(self, url):
        res = requests.get(url)
        data = res.content
        content_type = res.headers['content-type']
        ext = mimetypes.guess_extension(content_type)
        ext = '.jpg' if ext == '.jpe' else ext
        return data, ext

    def download_thumbnails_from_urls(self, urls, dest_folder='', verbose=False):
        if verbose:
            print('Downloading images in', dest_folder)
        nb_samples = len(urls)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        pattern = '0' + str(len(str(nb_samples)))
        progress = ''
        for i, url in enumerate(urls):
            try:
                data, ext = self.get_data_from_url(url)
                basename = format(i, pattern) + ext
                filepath = os.path.join(dest_folder, basename)
                with open(filepath, 'wb') as file:
                    file.write(data)
                if verbose:
                    progress = '\b' * len(progress) + '[{}/{}] {:.1%}'.format((i + 1), nb_samples, (i + 1) / nb_samples)
                    print(progress, end='', flush=True)
            except Exception as e:
                print('')
                print('Skipping url', url, 'because:', e)
                progress = ''
        if verbose:
            print('')

    def download_thumbnails_from_keywords(self, keywords, size=1, dest_folder='', verbose=True):
        for keyword in keywords:
            if verbose:
                print('Collecting:', keyword)
            urls = self.get_thumbnail_urls(keyword, size)
            if len(urls) == 0:
                if verbose:
                    print('!> cannot find any images for keyword', keyword)
                continue
            keyword_folder = keyword.replace(' ', '_')
            self.download_thumbnails_from_urls(urls, os.path.join(dest_folder, keyword_folder), verbose)
