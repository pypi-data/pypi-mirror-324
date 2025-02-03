import posixpath
import requests
import urllib.parse

API_START_PATH = "/api/v3/profiles/start/"
API_STOP_PATH = "/api/v3/profiles/close/"
API_CREATE_PATH = "/api/v3/profiles/create"
API_UPDATE_PROFILE_PATH = "/api/v3/profiles/update/"
API_PROFILE_LIST_PATH = "/api/v3/profiles"
API_DELETE_PATH = "/api/v3/profiles/delete/"
API_GROUPS_PATH = "/api/v3/groups"


class GPMLoginAPI:
    
    def __init__(self, api_url):
        self.api_url = api_url
    def urljoin(self, api_path, profile_id):
        url_path = posixpath.join(self.api_url, api_path, profile_id)
        return urllib.parse.urljoin(self.api_url, url_path)
    def start(self, profile_id, **kwargs):
        # profile_id
        # addination_args
        # win_scale
        # win_pos
        # win_size
        # params = {}
        url = self.urljoin(API_START_PATH, profile_id)
        return requests.get(url, params=kwargs).json()
    def stop(self, profile_id):
        #profile_id
        url = self.urljoin(API_STOP_PATH, profile_id)
        return requests.get(url).json()
    def delete(self, profile_id):
        url = self.urljoin(API_DELETE_PATH, profile_id)
        return requests.get(url).json()
    def update(self, profile_id, **kwargs):
        # profile_name
        # group_id
        # raw_proxy
        # startup_urls
        # note
        # color
        # user_agent
        url = self.urljoin(API_UPDATE_PROFILE_PATH, profile_id)
        return requests.get(url, params=kwargs).json()
    def get_groups(self):
        url = urllib.parse.urljoin(self.api_url, API_GROUPS_PATH)
        return requests.get(url).json()
    def get_profiles(self, **kwargs):
        # group_id
        # page
        # per_page
        # sort
        # search
        url = urllib.parse.urljoin(self.api_url, API_PROFILE_LIST_PATH)
        return requests.get(url, params=kwargs).json()
    def get_profile(self, profile_id):
        url = self.urljoin(API_PROFILE_LIST_PATH, profile_id)
        return requests.get(url).json()
# api = GPMLoginAPI("http://127.0.0.1:19995")
# print(api.get_groups())
