#!/usr/bin/env python3

from __future__ import annotations

from urllib.parse import urljoin

import requests

from urllib3.util import Retry
from requests.adapters import HTTPAdapter


class SaneJS():

    def __init__(self, root_url: str='https://sanejs.circl.lu/'):
        self.root_url = root_url
        self.session = requests.session()
        retries = Retry(total=5, backoff_factor=.1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))

    @property
    def is_up(self) -> bool:
        try:
            r = self.session.head(self.root_url)
            return r.status_code == 200
        except Exception:
            return False

    def sha512(self, sha512: str | list) -> dict[str, list[str]]:
        '''Search for a hash (sha512)
        Reponse:
            {
              "response": [
                "libraryname|version|filename",
                ...
              ]
            }
        '''
        r = self.session.post(urljoin(self.root_url, 'sha512'), json={'sha512': sha512})
        return r.json()

    def library(self, library: str | list, version: str | None=None) -> dict[str, dict[str, dict[str, dict[str, str]]]]:
        ''' Search for a library by name.
        Response:
            {
              "response": {
                "libraryname": {
                  "version": {
                    "filename": "sha512",
                    ...
                  }
                  ...
                },
                ...
              }
            }
        '''
        to_query = {'library': library}
        if version:
            to_query['version'] = version
        r = self.session.post(urljoin(self.root_url, 'library'), json=to_query)
        return r.json()
