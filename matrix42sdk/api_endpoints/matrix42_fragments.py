import json
import os
import requests
import sys
from matrix42sdk.AuthNClient import *


class GDSFragements(RestClient):
    def __init__(self, _path=None, _full_header=None, **kwargs):
        super().__init__(**kwargs)
        self._path = "/M42Services/api/data/fragments"
        self._full_header = self.get_matrix42_access_header()

        # print(self._full_header)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def get_fragement(self, ddname, fragmentid):
        """Reads the whole Fragment of the specified Data Definition with defined Id.

        Returns the JSON object with all attributes specified in the Data Definition.
        The Service returns null if the fragment with the specified fragmentId does not exist,
        or the Object the Fragment belongs to, is not allowed for the caller.
        """
        # full=true is important for getting complete object, including version
        req_url = self.url + self.path + "/%s/%s?full=true" % (ddname, fragmentid)
        print("Request URL for CI -> ", req_url)
        r_ci = requests.get(req_url, verify=self._ssl_verify, headers=self._full_header)
        r_ci.status_code
        # print(r_ci.text)
        return json.loads(r_ci.text)

    def update_fragement(self, ddname, jsonBody):
        """Updates the specified Data Definition fragment attributes.

        The Service modifies only attributes which are explicitly specified in the Request Body.
        The attributes which are not mentioned in the request are not affected by the Update operation.
        """
        # true => full update | must be same in the get method
        put_url = self.url + self.path + "/%s?full=true" % ddname
        print(put_url)

        r_ci_update = requests.put(
            put_url, verify=self._ssl_verify, headers=self._full_header, data=jsonBody
        )
        print(r_ci_update)
        if r_ci_update.status_code != 500:
            print("Update of CI fragment has been ok")

    def create_fragement(self, ddname, jsonBody):
        """Create method

        Do not use, untested
        """
        # true => full update | must be same in the get method
        put_url = self.url + self.path + "/%s?full=true" % ddname
        print(put_url)

        r_ci_update = requests.post(
            put_url, verify=False, headers=self._full_header, data=jsonBody
        )
        print(r_ci_update)
        if r_ci_update.status_code != 500:
            print("Update of CI fragment has been ok")

        return r_ci_update
