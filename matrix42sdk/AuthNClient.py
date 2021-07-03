import os
import requests
from matrix42sdk.Exceptions import AuthNError


MATRIX42_GENERATE_ACCESS_TOKEN_ENDPOINT = (
    "/m42Services/api/ApiToken/GenerateAccessTokenFromApiToken/"
)


class Matrix42RestClient(object):
    """Main Authentication Class

    Args:
        hostname (str): Full URL of ESM server, e.g. "https://matrix.firm.com"
        api_token (str): Generated API Token in the ESM GUI. Used for getting Access Token
        ssl_verify (bool): Requests' parameter for wherther TLS is being checked. Use it if hostname is using
                            Self-Signed Certificates
    """

    def __init__(
        self,
        _url=None,
        _api_token=None,
        _ssl_verify=False,
        _configKeyType=None,
    ):

        self._headers = dict({"Content-Type": "application/json"})
        self._ssl_verify = _ssl_verify
        self._url = _url
        self._configKeyType = _configKeyType
        self.__uses_shell = True
        self.__uses_app_token = True

        MATRIX42SDK_API_TOKEN = os.environ.get("MATRIX42SDK_API_TOKEN", None)
        MATRIX42_URL = os.environ.get("MATRIX42_URL", None)

        if MATRIX42_URL is None:
            self._url = _url.rstrip("/")
        elif MATRIX42_URL is not None:
            self._url = MATRIX42_URL.rstrip("/")
        else:
            raise AuthNError("URL is missing")

        if MATRIX42SDK_API_TOKEN is None:
            self._api_token = _api_token
        elif MATRIX42SDK_API_TOKEN is not None:
            self._api_token = MATRIX42SDK_API_TOKEN
        else:
            raise AuthNError(
                "All methods require to use either username/password or API Token."
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
    def set_access_token_header(
        cls, _headers, _url, _api_token, _ssl_verify, *args, **kwargs
    ):

        site_endpoint = _url + MATRIX42_GENERATE_ACCESS_TOKEN_ENDPOINT

        # dont use .update() on dict because it is updated in place, hence returning None type
        tkn_dict = dict({"Authorization": "Bearer %s" % _api_token})
        access_headers = dict(_headers, **tkn_dict)
        postReq = requests.post(
            site_endpoint, headers=access_headers, verify=_ssl_verify, *args, **kwargs
        )
        raw_acc_token = postReq.json()["RawToken"]

        # here we want to update in-place
        acc_tkn = dict({"Authorization": "Bearer %s" % raw_acc_token})
        _headers.update(**acc_tkn)
        return cls(_headers)

    def get_matrix42_access_header(self):
        if self.__uses_app_token is True:
            if self.__uses_shell is True:
                Matrix42RestClient.set_access_token_header(
                    self._headers, self._url, self._api_token, self._ssl_verify
                )
        return self._headers
