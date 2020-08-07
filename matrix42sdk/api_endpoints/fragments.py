import json
import requests
from matrix42sdk.AuthNClient import RestClient
from requests.exceptions import HTTPError


class FragmentsDataService(RestClient):
    """Fragments (/api/data/fragments), provides the operation for working with the Fragments (Instances of the Data Definitions)

    The Service provides methods for CRUD operations (Create-Read-Update-Delete) for Data Definitions presented in the Schema.

    Args:
        RestClient ([type]): Inherit RestClient object

    `URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/API%3A_Generic_Data_Service>`_
    """

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

    def delete_fragement(self, ddname, fragmentId):
        """Deletes the fragment from Database defined by the Data Definition name and the object ID.

        The operation is required for cases of multi-fragments or optional fragments.

        Args:
            ddname (str):
                The technical name of the Data Definition (e.g. SPSActivityClassBase)

            fragmentId (str):
                Id of the Fragment of specified Data Definition

        `URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Public_API_reference_documentation/Fragments_Data_Service:_Delete_Fragment>`_
        """
        req_url = self.url + self.path + "/%s/%s" % (ddname, fragmentId)
        try:
            r_ci_del = requests.delete(
                req_url, verify=self._ssl_verify, headers=self._full_header
            )
            r_ci_del.raise_for_status()
            return r_ci_del

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except Exception as err:
            print(f"Other error occurred: {err}")

    def get_fragment(self, ddname, fragmentId):
        """Reads the whole Fragment of the specified Data Definition with defined Id.

        Returns:
            Returns the JSON object with all attributes specified in the Data Definition.
            The Service returns null if the fragment with the specified fragmentId does not exist,
            or the Object the Fragment belongs to, is not allowed for the caller.

        Args:
            ddname (str):
                The technical name of the Data Definition (e.g. SPSActivityClassBase)

            fragmentId (str):
                Id of the Fragment of specified Data Definition

        `Matrix42 URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Public_API_reference_documentation/Fragments_Data_Service%3A_Get_Fragment_data>`_

        """
        # full=true is important for getting complete object, including version
        req_url = self.url + self.path + "/%s/%s?full=true" % (ddname, fragmentId)
        try:
            r_ci = requests.get(
                req_url, verify=self._ssl_verify, headers=self._full_header
            )
            r_ci.raise_for_status()
            return json.loads(r_ci.text)

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except Exception as err:
            print(f"Other error occurred: {err}")

    # https://docs.python.org/3/tutorial/controlflow.html#special-parameters
    # only allows keyword arguments as indicated
    def get_fragments_list(
        self,
        ddname,
        *,
        where=None,
        columns=None,
        pageSize=None,
        pageNumber=None,
        sort=None,
        includeLocalizations=None,
    ):
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
                Optional. Sets the number of records (fragments) returned by Operation. Used in combination with the PageNumber parameter
            pageNumber (int):
                Optional. Sets the Number of the page. Used in combination with `pageSize` property.
            sort (str):
                Optional. Defines the sorting in the result. Example: "Name ASC, CreatedDate DESC"
            includeLocalizations (bool):
                Optional. Specifies if the Localization table should be included in the result. The parameter works ONLY
                with the request with "schema-info" directive. The service handles correctly only attributes of the
                requested Data Definition. Related attributes which are part of the response, but not
                in Data Definition (e.g. SPSActivityClassBase: Category.Name) keep only values of the request culture.
                If you need all localizations for these attributes as well, please run a dedicated request to Data
                Definition which keeps this attribute (e.g. SPSScCategoryClassBase)

        `URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Public_API_reference_documentation/Fragments_Data_Service%3A_Get_a_list_of_Fragments>`_

        """
        req_url = self.url + self.path + "/%s" % ddname

        payload = dict()
        if where is not None:
            payload.update({"where": where})
        if columns is not None:
            payload.update({"columns": columns})
        if pageSize is not None:
            payload.update({"pageSize": pageSize})
        if pageNumber is not None:
            payload.update({"pageNumber": pageNumber})
        if sort is not None:
            payload.update({"sort": sort})
        if includeLocalizations is not None:
            payload.update({"includeLocalizations": includeLocalizations})

        try:
            r_ci_list = requests.get(
                req_url,
                params=payload,
                verify=self._ssl_verify,
                headers=self._full_header,
            )
            r_ci_list.raise_for_status()
            return json.loads(r_ci_list.text)

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except Exception as err:
            print(f"Other error occurred: {err}")

    def get_fragment_relations_list(
        self,
        ddname,
        fragmentId,
        relationName,
        *,
        where=None,
        columns=None,
        pageSize=None,
        pageNumber=None,
        sort=None,
        includeLocalizations=None,
    ):
        """Retrieves a list of fragment's relations with a defined list of columns which match the specified search
        criteria and are sorted in the defined order.

        Returns:
            Retrieves a list of fragments with a defined list of columns which match the specified
            search criteria and are sorted in the defined order. In case of need, the method returns
            the schema metadata for the returned data.

            An array of JSON objects where each object represents the Data Definition fragment which matches
            the specified search criteria and is allowed for the current user (caller).

        Args:
            ddname (str):
                Required. The technical name of the Data Definition (e.g. SPSActivityClassBase)
            fragmentId (str):
                Required. Id of the Fragment of specified Data Definition
            relationName (str):
                Required. Technical name of the relation (e.g. AttachedUsers).
            where (str):
                Optional. A-SQL Where Expression. If no filtering expression is specified, the Service returns all fragments
                of the specified Data Definition which are allowed for the caller.
            columns (str):
                Optional. A-SQL Column expression defines the columns in the result set, separated by Comma. If no Columns defines,
                then the Operation returns only Fragment Ids. Example: Name, Parent.Name as ParentName
            pageSize (int):
                Optional. Sets the number of records (fragments) returned by Operation. Used in combination with the PageNumber parameter
            pageNumber (int):
                Optional. Sets the Number of the page. Used in combination with `pageSize` property.
            sort (str):
                Optional. Defines the sorting in the result. Example: "Name ASC, CreatedDate DESC"
            includeLocalizations (bool):
                Optional. Specifies if the Localization table should be included in the result. The parameter works ONLY
                with the request with "schema-info" directive. The service handles correctly only attributes of the
                requested Data Definition. Related attributes which are part of the response, but not
                in Data Definition (e.g. SPSActivityClassBase: Category.Name) keep only values of the request culture.
                If you need all localizations for these attributes as well, please run a dedicated request to Data
                Definition which keeps this attribute (e.g. SPSScCategoryClassBase)

        `URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Public_API_reference_documentation/Fragments_Data_Service%3A_Get_a_list_of_Fragment_Relations>`_

        """
        req_url = self.url + self.path + "/%s/%s/%s" % (ddname, fragmentId, relationName)

        payload = dict()
        if where is not None:
            payload.update({"where": where})
        if columns is not None:
            payload.update({"columns": columns})
        if pageSize is not None:
            payload.update({"pageSize": pageSize})
        if pageNumber is not None:
            payload.update({"pageNumber": pageNumber})
        if sort is not None:
            payload.update({"sort": sort})
        if includeLocalizations is not None:
            payload.update({"includeLocalizations": includeLocalizations})

        try:
            r_ci_list = requests.get(
                req_url,
                params=payload,
                verify=self._ssl_verify,
                headers=self._full_header,
            )
            r_ci_list.raise_for_status()
            return json.loads(r_ci_list.text)

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except Exception as err:
            print(f"Other error occurred: {err}")

    def create_fragment(self, ddname, jsonBody):
        """Creates a new Data Definition fragment. The operation is required for cases of multi-fragments or optional fragments.

        Args:
            ddname (str):
                Required. The technical name of the Data Definition (e.g. SPSActivityClassBase)
            jsonBody: (json)
                Request Body with a JSON containing all necessary data for Fragment creation.
                For JSON  structure examples see  Fragments Data Service: Get Fragment page.

        Returns:
            Id of the created Fragment.

        `URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Public_API_reference_documentation/Fragments_Data_Service%3A_Create_Fragment>`_

        Untested
        """
        put_url = self.url + self.path + "/%s" % ddname
        try:
            r_ci_create = requests.post(
                put_url, verify=self._ssl_verify, headers=self._full_header, data=jsonBody
            )
            r_ci_create.raise_for_status()
            return r_ci_create

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except Exception as err:
            print(f"Other error occurred: {err}")

    def update_fragment(self, ddname, jsonBody):
        """Updates the specified Data Definition fragment attributes.

        The Service modifies only attributes which are explicitly specified in the Request Body.
        The attributes which are not mentioned in the request are not affected by the Update operation.

        Needs jsonBody which has "JSON Object with fragment attributes with new values".

        Use :meth:`get_fragment <matrix42sdk.FragmentsDataService.get_fragment>` JSON object to update fields.

        JSON object should contain:
            ID (str): Attribute with the updated Fragment Id value is required.
            Concurrency tracking (str): if you want to track concurrency also include the TimeStamp attribute.
            Reset the attribute value (str): in case you want to reset the attribute value add this attribute to JSON object with the value null.

        Returns:
            The system returns no data, but this method returns Requests' full `put` object.

        `URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Public_API_reference_documentation/Fragments_Data_Service%3A_Update_fragment>`_

        """
        # true => full update | must be same in the get method
        put_url = self.url + self.path + "/%s?full=true" % ddname

        try:
            r_ci_update = requests.put(
                put_url, verify=self._ssl_verify, headers=self._full_header, data=jsonBody
            )
            r_ci_update.raise_for_status()

            if r_ci_update.status_code == 204:
                print("Update of CI fragment has been ok")

            return r_ci_update

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except Exception as err:
            print(f"Other error occurred: {err}")

    def delete_fragment_relation(
        self, ddname, fragmentId, relationName, relationFragmentId
    ):
        """Deletes the relation from Database defined by Data Definition name, fragment ID and Relation name.

        The operation is required for managing many-to-many relations.

        Returns:
            The system returns no data, but this method returns Requests' full `post` object.

        Args:
            ddname (str):
                The technical name of the Data Definition (e.g. SPSActivityClassBase)
            fragmentid (str):
                Id of the Fragment of specified Data Definition
            relationName (str):
                Technical name of the relation (e.g. AttachedUsers).
            relationFragmentId (str):
                Id of the Data Definition's fragment that is added as a relation.

        `Matrix42 URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Public_API_reference_documentation/Fragments_Data_Service%3A_Delete_Fragment_Relation>`_

        """
        req_url = (
            self.url
            + self.path
            + "/%s/%s/%s/%s" % (ddname, fragmentId, relationName, relationFragmentId)
        )
        try:
            r_ci_delete_rel = requests.delete(
                req_url, verify=self._ssl_verify, headers=self._full_header
            )
            r_ci_delete_rel.raise_for_status()
            return r_ci_delete_rel

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except Exception as err:
            print(f"Other error occurred: {err}")

    def add_fragment_relation(self, ddname, fragmentId, relationName, relationFragmentId):
        """Adds relation to the Database defined by Data Definition name, fragment ID and Relation name.

        The operation is required for managing many-to-many relations.
        The operation adds a single object to relation. If you need to add multiple relations to the object,
        you need to make a call of the Service for each of them

        Returns:
            The system returns no data, but this method returns Requests' full `post` object.

        Args:
            ddname (str):
                The technical name of the Data Definition (e.g. SPSActivityClassBase)
            fragmentid (str):
                Id of the Fragment of specified Data Definition
            relationName (str):
                Technical name of the relation (e.g. AttachedUsers).
            relationFragmentId (str):
                Id of the Data Definition's fragment that is added as a relation.

        `Matrix42 URL <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Public_API_reference_documentation/Fragments_Data_Service%3A_Add_Fragment_Relation>`_

        """
        req_url = (
            self.url
            + self.path
            + "/%s/%s/%s/%s" % (ddname, fragmentId, relationName, relationFragmentId)
        )
        try:
            r_ci_add_rel = requests.get(
                req_url, verify=self._ssl_verify, headers=self._full_header
            )
            r_ci_add_rel.raise_for_status()
            return r_ci_add_rel

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except Exception as err:
            print(f"Other error occurred: {err}")
