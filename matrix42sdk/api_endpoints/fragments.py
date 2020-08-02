import json
import requests
from matrix42sdk.AuthNClient import *


class FragmentsDataService(RestClient):
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

    def get_fragment(self, ddname, fragmentid):
        """Reads the whole Fragment of the specified Data Definition with defined Id.

        Returns:
            Returns the JSON object with all attributes specified in the Data Definition.
            The Service returns null if the fragment with the specified fragmentId does not exist,
            or the Object the Fragment belongs to, is not allowed for the caller.

        Args:
            ddname (str):
                The technical name of the Data Definition (e.g. SPSActivityClassBase)

            fragmentid (str):
                Id of the Fragment of specified Data Definition

        `URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Public_API_reference_documentation/Fragments_Data_Service%3A_Get_Fragment_data>`_

        """
        # full=true is important for getting complete object, including version
        req_url = self.url + self.path + "/%s/%s?full=true" % (ddname, fragmentid)
        r_ci = requests.get(req_url, verify=self._ssl_verify, headers=self._full_header)
        r_ci.status_code
        return json.loads(r_ci.text)

    def get_fragment_list(self, ddname):
        """Retrieves a list of fragments with a defined list of columns, which match the specified search criteria.

        Returns:
            Retrieves a list of fragments with a defined list of columns which match the specified
            search criteria and are sorted in the defined order. In case of need, the method returns
            the schema metadata for the returned data.

            An array of JSON objects where each object represents the Data Definition fragment which matches
            the specified search criteria and is allowed for the current user (caller).

        Args:
            ddname (str):
                Required. The technical name of the Data Definition (e.g. SPSActivityClassBase)
            where (str):
                Optional. A-SQL Where Expression. If no filtering expression is specified, the Service returns all fragments
                of the specified Data Definition which are allowed for the caller.
            columns (str):
                Optional. A-SQL Column expression defines the columns in the result set, separated by Comma. If no Columns defines,
                then the Operation returns only Fragment Ids. Example: Name, Parent.Name as ParentName
            pageSize (int):
                Sets the number of records (fragments) returned by Operation. Used in combination with the PageNumber parameter
            pageNumber (int):
                Sets the Number of the page. Used in combination with `pageSize` property.
            Sort (str):
                Defines the sorting in the result. Example: "Name ASC, CreatedDate DESC"
            includeLocalizations (bool):
                Specifies if the Localization table should be included in the result. The parameter works ONLY with the request with "schema-info" directive. The service handles correctly only attributes of the requested Data Definition. Related attributes which are part of the response, but not in Data Definition (e.g.  SPSActivityClassBase: Category.Name) keep only values of the request culture. If you need all localizations for these attributes as well, please run a dedicated request to Data Definition which keeps this attribute (e.g. SPSScCategoryClassBase)

        `URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Public_API_reference_documentation/Fragments_Data_Service%3A_Get_a_list_of_Fragments>`_

        """
        req_url = self.url + self.path + "/%s/%s?full=true" % ddname
        r_ci = requests.get(req_url, verify=self._ssl_verify, headers=self._full_header)
        return

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

