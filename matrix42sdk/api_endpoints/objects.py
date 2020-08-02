import json
import requests
from matrix42sdk.AuthNClient import RestClient


class ObjectsDataService(RestClient):
    """Objects (/api/data/objects) which addresses operations with the Objects (instances of the Configuration Items)

    The Service provides methods for CRUD operations (Create-Read-Update-Delete) for Configuration Items presented in the Schema.

    Args:
        RestClient ([type]): Inherit RestClient object

    `URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/API%3A_Generic_Data_Service>`_
    """

    def __init__(self, _path=None, _full_header=None, **kwargs):
        super().__init__(**kwargs)
        self._path = "/M42Services/api/data/objects"
        self._full_header = self.get_matrix42_access_header()
        # print(self._full_header)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def get_object(self, entity, objectid):
        """Return JSON object

        Reads the whole Object with the specified Configuration Item name and object ID.
        The Service returns exclusively the data belonged to object (e.g. attributes, N:1 relations)
        Virtual attributes, like N:M relations are not returned and need to
        be obtained with the dedicated service request
        """
        # full=true is important for getting complete object, including version
        req_url = self.url + self.path + "/%s/%s?full=true" % (entity, objectid)
        r_ci = requests.get(req_url, verify=self._ssl_verify, headers=self._full_header)
        r_ci.status_code
        return json.loads(r_ci.text)

    def update_object(self, entity, jsonBody):
        """
            Updates the object of the specified Configuration Item name and object ID.
            The method works in pair with Get Object method, which delivers the original
            Object with the current Timestamp (market of current state), which is used for
            concurrency tracking.
        """
        # true => full update | must be same in the get method
        put_url = self.url + self.path + "/%s?full=true" % entity
        # print(put_url)

        r_ci_update = requests.put(
            put_url, verify=self._ssl_verify, headers=self._full_header, json=jsonBody
        )
        if r_ci_update.status_code != 500:
            print("Update of CI object has been ok")
