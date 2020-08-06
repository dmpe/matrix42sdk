import json
import requests
from matrix42sdk.AuthNClient import RestClient
from requests.exceptions import HTTPError


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

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def get_object(self, ciName, objectId, full="true"):
        """Gets the whole Object with the specified Configuration Item name and object ID.

        The Service returns exclusively the data belonged to object (e.g. attributes, N:1 relations).
        Virtual attributes, like N:M or 0/1 to N relations are not returned and need to be obtained
        with the additional Web Service request.

        TimeStamp is a special marker is used for the concurrency issues handling on modifying the Fragment.
        TimeStamp is generated for each Object Fragment.

        Args:
            ciName (str):
                Required. Technical name of the Configuration Item (e.g. for Incident is "SPSActivityTypeIncident")
            objectId (str):
                Required. Id of the Object of specified Configuration Item
            full (str):
                Optional. Signals to load the whole Object with all related multi-fragments data, otherwise, all multi-fragments are omitted.
                While Rest API defaults to 'false', this SDK does 'true'.

        Returns:
            The whole Object with all defined Data Definitions and attributes. The
            Multi-fragments are present only when parameter full is set.

        `URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Public_API_reference_documentation/Objects_Data_Service%3A_Get_Object_data>`_
        """
        # full=true is important for getting complete object, including version
        req_url = self.url + self.path + "/%s/%s?full=%s" % (ciName, objectId, full)
        try:

            r_ci_get = requests.get(
                req_url, verify=self._ssl_verify, headers=self._full_header
            )
            r_ci_get.raise_for_status()

            if r_ci_get.status_code == 400:
                return Exception(
                    "The object with the specified Configuration Item and Object ID is not present, or not allowed for the caller."
                )

            return json.loads(r_ci_get.text)

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except Exception as err:
            print(f"Other error occurred: {err}")

    def update_object(self, ciName, jsonBody, full="true"):
        """Updates the object of the specified Configuration Item name and object ID.

        The method works in pair with Get Object method, which delivers the original
        Object with the current Timestamp (market of current state), which is used for
        concurrency tracking.

        Returns:
            The server does not return any data. Nonetheless, we return the Request's object.

        Args:
            ciName (str):
                Required. Technical name of the Configuration Item (e.g. for Incident is "SPSActivityTypeIncident")
            objectid (str):
                Required. Id of the Object of specified Configuration Item
            full (str):
                Optional. Signals to load the whole Object with all related multi-fragments data, otherwise, all multi-fragments are omitted.
                While Rest API defaults to 'false', this SDK does 'true'.

        `URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Public_API_reference_documentation/Object_Data_Service%3A_Update_Object>`_

        """
        # true => full update | must be same in the get method
        put_url = self.url + self.path + "/%s?full=%s" % (ciName, full)

        try:
            r_ci_update = requests.put(
                put_url, verify=self._ssl_verify, headers=self._full_header, json=jsonBody
            )
            r_ci_update.raise_for_status()

            if r_ci_update.status_code == 500:
                return Exception(
                    "Concurrency. The object you want to update has been updated by another process!"
                )

            return r_ci_update

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except Exception as err:
            print(f"Other error occurred: {err}")

    def create_object(self, ciName, jsonBody):
        """Creates a new Object of the specified Configuration Item.

        If needed it is possible explicitly set IDs for the created Object or related fragments.
        If IDs are omitted in the Request, they are auto-generated

        Returns:
            Guid. ID of the Created Object

        Args:
            ciName (str):
                Technical name of the Configuration Item (e.g. for Incident is "SPSActivityTypeIncident")

        `URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Public_API_reference_documentation/Object_Data_Service%3A_Create_Object>`_
        """
        put_url = self.url + self.path + "/%s" % ciName
        try:

            r_ci_create = requests.post(
                put_url, verify=self._ssl_verify, headers=self._full_header, json=jsonBody
            )
            r_ci_create.raise_for_status()

            if r_ci_create.status_code == 401:
                return Exception("Unauthorized")
            elif r_ci_create.status_code == 415:
                return Exception("The request Content-type is not defined")
            elif r_ci_create.status_code == 500:
                return Exception(
                    "Internal Server Error. E.g. wrong reference, or mandatory attribute is missing"
                )
            else:
                return r_ci_create

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except Exception as err:
            print(f"Other error occurred: {err}")

    def delete_object(self, ciName, objectId):
        """Deletes the object from Database defined by the Configuration Item name and the object ID.

        Returns:
            The server does not return any data. Nonetheless, we return the Request's object.

        Args:
            ciName (str):
                Required. Technical name of the Configuration Item (e.g. for Incident is "SPSActivityTypeIncident")
            objectId (str):
                Required. Id of the Object of specified Configuration Item

        `URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Public_API_reference_documentation/Object_Data_Service%3A_Create_Object>`_
        """
        put_url = self.url + self.path + "/%s" % ciName
        try:

            r_ci_delete = requests.delete(
                put_url, verify=self._ssl_verify, headers=self._full_header
            )
            r_ci_delete.raise_for_status()

            return r_ci_delete

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except Exception as err:
            print(f"Other error occurred: {err}")
