"""Fellow object to interact with Aiden brewer."""
import json
import logging
import re
import requests
import sys
from difflib import SequenceMatcher
from fellow_aiden.profile import CoffeeProfile
from pydantic import ValidationError


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

    
class FellowAiden:
    
    """Fellow object to interact with Aiden brewer."""

    NAME = "FELLOW-AIDEN"
    LOG_LEVEL = logging.DEBUG
    INTERVAL = 0.5
    BASE_URL = 'https://l8qtmnc692.execute-api.us-west-2.amazonaws.com/v1'
    API_AUTH = '/auth/login'
    API_DEVICES = '/devices'
    API_DEVICE = '/devices/{id}'
    API_PROFILES = '/devices/{id}/profiles'
    API_PROFILE = '/devices/{id}/profiles/{pid}'
    API_PROFILE_SHARE = '/devices/{id}/profiles/{pid}/share'
    API_SHARED_PROFILE = '/shared/{bid}'
    HEADERS = {
        'User-Agent': 'Fellow/5 CFNetwork/1568.300.101 Darwin/24.2.0'
    }
    SERVER_SIDE_PROFILE_FIELDS = [
        'id',
        'createdAt',
        'deletedAt',
        'lastUsedTime',
        'sharedFrom',
        'isDefaultProfile',
        'instantBrew',
        'folder',
        'duration',
        'lastGBQuantity'
    ]
    SESSION = requests.Session()
    

    def __init__(self, email, password):
        """Start of self."""
        self._log = self._logger()
        self._auth = False
        self._token = None
        self._refresh = None
        self._email = email
        self._password = password
        self._device_config = None
        self._brewer_id = None
        self.__auth()
        
    def _logger(self):
        """Create a logger to be used between processes.

        :returns: Logging instance.
        """
        logger = logging.getLogger(self.NAME)
        logger.setLevel(self.LOG_LEVEL)
        shandler = logging.StreamHandler(sys.stdout)
        fmt = '\033[1;32m%(levelname)-5s %(module)s:%(funcName)s():'
        fmt += '%(lineno)d %(asctime)s\033[0m| %(message)s'
        shandler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(shandler)
        return logger
        
    def __auth(self):
        self._log.debug("Authenticating user")
        auth = {"email": self._email, "password": self._password}
        self.SESSION.headers.update(self.HEADERS)
        login_url = self.BASE_URL + self.API_AUTH
        response = self.SESSION.post(login_url, json=auth, headers=self.HEADERS)
        parsed = json.loads(response.content)
        self._log.debug(parsed)
        if 'accessToken' not in parsed:
            raise Exception("Email or password incorrect.")
        self._log.debug("Authentication successful")
        self._token = parsed['accessToken']
        self._refresh = parsed['refreshToken']
        self.SESSION.headers.update({'Authorization': 'Bearer ' + self._token})
        self._auth = True
        # Makes sense to populate the device as it's used in subsequent calls
        self.__device()
        
    def __device(self):
        self._log.debug("Fetching device for account")
        device_url = self.BASE_URL + self.API_DEVICES
        response = self.SESSION.get(device_url, params={'dataType': 'real'})
        parsed = json.loads(response.content)
        self._device_config = parsed[0]  # Assumes single brewer per account
        self._brewer_id = self._device_config['id']
        self._profiles = self._device_config['profiles']
        self._log.debug("Brewer ID: %s" % self._brewer_id)
        self._log.info("Device and profile information set")

    def parse_brewlink_url(self, link):
        """Extract profile information from a shared brew link."""
        self._log.debug("Parsing shared brew link")
        pattern = r'(?:.*?/p/)?([a-zA-Z0-9]+)/?$'
        match = re.search(pattern, link)
        if not match:
            raise ValueError("Invalid profile URL or ID format")
        brew_id = match.group(1)
        self._log.debug("Brew ID: %s" % brew_id)
        shared_url = self.BASE_URL + self.API_SHARED_PROFILE.format(bid=brew_id)
        response = self.SESSION.get(shared_url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch profile (ID: {brew_id})")
        parsed = json.loads(response.content)
        for field in self.SERVER_SIDE_PROFILE_FIELDS:
            parsed.pop(field, None)
        self._log.debug("Profile fetched: %s" % parsed)
        return parsed
    
    def get_device_config(self, remote=False):
        """Return the current device config.

        :param remote: If True, force a new request to Fellow's API
                    to refresh the device config. Otherwise,
                    returns the cached config.
        """
        if remote:
            self.__device()
        return self._device_config

        
    def get_display_name(self):
        return self._device_config.get('displayName', None)
        
    def get_profiles(self):
        return self._profiles
    
    def get_profile_by_title(self, title, fuzzy=False):
        for profile in self._profiles:
            if fuzzy:
                if similar(profile['title'].lower(), title.lower()) > 0.65:
                    return profile
            if profile['title'].lower() == title.lower():
                return profile
        return None
        
    def get_brewer_id(self):
        return self._brewer_id
        
    def create_profile(self, data):
        self._log.debug("Checking brew profile: %s" % data)
        try:
            CoffeeProfile.model_validate(data)
        except ValidationError as err:
            self._log.error("Brew profile format was invalid: %s" % err)
        if 'id' in data.keys():
            raise Exception("Candidate profiles must be free of server derived fields.")
        self._log.debug("Brew profile passed checks")
        profile_url = self.BASE_URL + self.API_PROFILES.format(id=self._brewer_id)
        response = self.SESSION.post(profile_url, json=data)
        parsed = json.loads(response.content)
        if 'id' not in parsed:
            raise Exception("Error in processing: %s" % parsed)
        self.__device()  # Refreshed profiles this way
        self._log.debug("Brew profile created: %s" % parsed)
        return parsed

    def create_profile_from_link(self, link):
        """Create a profile from a shared brew link."""
        self._log.debug("Creating profile from link")
        data = self.parse_brewlink_url(link)
        return self.create_profile(data)
    
    def generate_share_link(self, pid):
        """Generate a share link for a profile."""
        self._log.debug("Generating share link")
        share_url = self.BASE_URL + self.API_PROFILE_SHARE.format(id=self._brewer_id, pid=pid)
        self._log.debug("Share URL: %s" % share_url)
        response = self.SESSION.post(share_url)
        parsed = json.loads(response.content)
        if 'link' not in parsed:
            raise Exception("Error in processing: %s" % parsed)
        self._log.debug("Share link generated: %s" % parsed)
        return parsed['link']
        
    def delete_profile_by_id(self, pid):
        self._log.debug("Deleting profile")
        found = False
        for profile in self._profiles:
            if pid == profile['id']:
                found = True
        if not found:
            raise Exception("Profile does not exist")
        delete_url = self.BASE_URL + self.API_PROFILE.format(id=self._brewer_id, pid=pid)
        response = self.SESSION.delete(delete_url)
        self._log.info("Profile deleted")
        return True
    
    def adjust_setting(self, setting, value):
        patch_url = self.BASE_URL + self.API_DEVICE.format(id=self._brewer_id)
        data = json.dumps({setting: value})
        response = self.SESSION.patch(patch_url, data=data)
        parsed = json.loads(response.content)
        return parsed
        
    def authenticate(self):
        """
        Public method to reauthenticate the user.

        This allows external callers (like HA integration) to trigger
        reauthentication without accessing the private __auth method.
        """
        self._log.debug("Reauthenticating user via public method")
        self.__auth()
