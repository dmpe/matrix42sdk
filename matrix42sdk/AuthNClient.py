import os
import requests
import urllib3
from configparser import ConfigParser
from matrix42sdk.Exceptions import *


urllib3.disable_warnings()
MATRIX42_GENERATE_ACCESS_TOKEN_ENDPOINT = (
    "/m42Services/api/ApiToken/GenerateAccessTokenFromApiToken/"
)


class RestClient(object):
    """Main Authentication Class

    Args:
        hostname (str): Full URL of ESM server, e.g. "https://matrix.firm.com"
        api_token (str): Generated API Token in ESM GUI, to be used for getting Access Token
        ssl_verify (bool): Requests' parameter for wherther TLS is being checked. Use if hosted using
        Self-Signed Certificates
    """

    def __init__(
        self,
        _url=None,
        _api_token=None,
        _ssl_verify=False,
        _configIni=None,
        _configKeyType=None,
    ):

        self._headers = dict({"Content-Type": "application/json"})
        self._ssl_verify = _ssl_verify
        self._url = _url
        self._configIni = _configIni
        self._configKeyType = _configKeyType
        self.__uses_shell = True
        self.__uses_app_token = True

        MATRIX42SDK_API_TOKEN = os.environ.get("MATRIX42SDK_API_TOKEN", None)
        MATRIX42_URL = os.environ.get("MATRIX42_URL", None)

        # if MATRIX42SDK_API_TOKEN is None:
        #     if MATRIX42_URL is None:
        #         self.__uses_shell = False

        #     if self._configIni not in (None, "") or self._configKeyType not in (None, ""):
        #         self.__uses_shell = False # uses ini file
        #         print(" we use config files")

        if MATRIX42_URL is None:
            self._url = _url.rstrip("/")
        elif MATRIX42_URL is not None:
            self._url = MATRIX42_URL.rstrip("/")
        else:
            raise APIKeyMissingError("URL is missing")

        if MATRIX42SDK_API_TOKEN is None:
            self._api_token = _api_token
        elif MATRIX42SDK_API_TOKEN is not None:
            self._api_token = MATRIX42SDK_API_TOKEN
        else:
            raise APIKeyMissingError(
                "All methods will require to use either username/password" "or API Token."
            )

    def __str__(self):
        for attribute, value in self.__dict__.items():
            print(attribute, " => ", value)
        return ""

    @property
    def ssl_verify(self):
        return self._ssl_verify

    @ssl_verify.setter
    def ssl_verify(self, value):
        self._ssl_verify = value

    @property
    def configIni(self):
        return self._configIni

    @configIni.setter
    def configIni(self, value):
        self._configIni = value

    @property
    def api_token(self):
        return self._api_token

    @api_token.setter
    def api_token(self, value):
        self._api_token = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @classmethod
    def set_access_token_header(cls, _headers, _url, _api_token, _ssl_verify):

        site_endpoint = _url + MATRIX42_GENERATE_ACCESS_TOKEN_ENDPOINT

        # dont use .update() on dict because it is updated in place, hence returning None type
        tkn_dict = dict({"Authorization": "Bearer %s" % _api_token})
        access_headers = dict(_headers, **tkn_dict)
        # print("access headers after being updated: ", access_headers)
        rm = requests.post(site_endpoint, headers=access_headers, verify=_ssl_verify)
        raw_acc_token = rm.json()["RawToken"]

        # here we want to update in-place
        acc_tkn = dict({"Authorization": "Bearer %s" % raw_acc_token})
        _headers.update(**acc_tkn)
        # print("new headers finally: ", _headers)
        return cls(_headers)

    def get_matrix42_access_header(self):
        print("in get_matrix42_access_token the method")
        if self.__uses_app_token is True:
            print("we use app token")
            if self.__uses_shell is True:
                RestClient.set_access_token_header(
                    self._headers, self._url, self._api_token, self._ssl_verify
                )
            # else:
            #     RestClient.readConfigIni(self._configIni, self._configKeyType)
            #     RestClient.set_access_token_header(self._headers, self._url, self._api_token, self._ssl_verify)

        # print("print final headers -> ", self._headers)
        # print(MATRIX42_URL, "  ", MATRIX42SDK_API_TOKEN)
        return self._headers

    @classmethod
    def readConfigIni(cls, _configIni, _configKeyType):
        configparser = ConfigParser()
        print("_configKeyType: ", _configKeyType)
        configparser.read(_configIni)
        print("sections: ", configparser.sections())
        print("new: -> ", configparser[_configKeyType]["MATRIX42_URL"])
        return cls(
            _url=configparser[_configKeyType]["MATRIX42_URL"],
            _api_token=configparser[_configKeyType]["MATRIX42SDK_API_TOKEN"],
        )
