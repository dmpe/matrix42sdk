import json
import logging
import matrix42sdk
import os
import pprint
import pytest
import random
import sys
from matrix42sdk import AuthNClient
from matrix42sdk.api_endpoints import matrix42_fragments, matrix42_objects


JUPYTERLAB_ID = "fa328004-9816-cda5-927a-08d82fde9cbd"
JUPYTERLAB_ID_FRAG = "8c51cfff-bf16-452e-8d2c-527cc25518c3"
SYS_ENTITY = "SPSSoftwareType"
SYS_FRAGEMENT = "Ud_SoftwareproduktVersionClassBase"

logging.basicConfig()


class TestMatrix42ESM_Basic:
    @pytest.fixture(autouse=True)
    def setup_method_fix(self, get_url, get_api_token):
        self.get_url = get_url
        self.get_api_token = get_api_token

    def test_RestClient_simpleInput(self):
        a = AuthNClient.RestClient(_url=self.get_url)
        a.ssl_verify = False
        assert a.ssl_verify == False
        assert a.url == self.get_url


class TestMatrix42ESM_ObjectsManipulation:
    @pytest.fixture(autouse=True)
    def setup_method_fix(self, get_url, get_api_token):
        self.get_url = get_url
        self.get_api_token = get_api_token

    def test_RestClient_shell_url_token(self):
        matc = AuthNClient.RestClient(_url=self.get_url, _api_token=self.get_api_token)
        assert len(matc.api_token) >= 300
        assert matc.url.startswith("https://")


class TestMatrix42ESM_FragmentsManipulation:
    @pytest.fixture(autouse=True)
    def setup_method_fix(self, get_url, get_api_token):
        self.get_url = get_url
        self.get_api_token = get_api_token

    def test_get_Fragement_pure_shell_getJupyterFragement(self):
        mat = matrix42_fragments.GDSFragements()
        full_ci_frg = mat.get_fragement(SYS_FRAGEMENT, JUPYTERLAB_ID_FRAG)
        pprint.pprint(full_ci_frg)

    def test_update_Fragement_shell(self):
        main_vers = random.randint(1, 9)
        version = str(main_vers) + ".0.5"
        print("\nversion numbers", version)

        mat = matrix42_fragments.GDSFragements()
        full_ci_frg = mat.get_fragement(SYS_FRAGEMENT, JUPYTERLAB_ID_FRAG)

        id = full_ci_frg["ID"]
        time = full_ci_frg["TimeStamp"]
        versionState = full_ci_frg["VersionState"]

        data_set = {
            "ID": id,
            "TimeStamp": time,
            "Version": version,
            "VersionState": versionState,
        }
        json_dump = json.dumps(data_set)
        mat.update_fragement(SYS_FRAGEMENT, json_dump)
