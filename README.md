# Python3 Matrix42 SDK for Enterprise Service Management (ESM) tool

"ERP for Software Asset Management"

[![matrix42sdk package in my-feed feed in Azure Artifacts](https://feeds.dev.azure.com/johnmalc/2efa647f-e5a5-4720-835d-4fc45fde9432/_apis/public/Packaging/Feeds/0c65acb4-f8ae-4df6-9f17-9db0f7687350/Packages/313927f6-82a5-4f2b-9bb0-9b90bcf3cec2/Badge)](https://dev.azure.com/johnmalc/Matrix42SDK/_packaging?_a=package&feed=0c65acb4-f8ae-4df6-9f17-9db0f7687350&package=313927f6-82a5-4f2b-9bb0-9b90bcf3cec2&preferRelease=true)

## The background story

As of July 2020, Matrix42 AG, a German company is offering a [Configuration Management Database (CMBD)](https://www.matrix42.com/en/digital-workspace-management/enterprise-service-management) - basically a competing product to ServiceNOW and many others like MSFT Intune.

Their Angular based product can be installed on-prem and used as ITIL supporting tool for the company.

It provides a REST API which this Python3+ SDK tries to cover.
Unfortunately, Swagger support is currently not available which has led me to write this client package myself - becoming my first python3 client SDK.

It shows - also due to learning Python OOP principles.

### Documentation of Rest API

- <https://help.matrix42.com/030_DWP/030_INT> Intro
- <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations> How to use the API
- <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Matrix42_Web_Services_API> Matrix42 Approach to the API
- <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Web_Services%3A_Authentication_types> Example of AuthN
- <https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Web_Services_tokens%3A_Generate_API_Token> Generate API Token

# Matrix42 SDK for Python

To use Matrix42 SDK, first decide which authN approach you are going to use.

For a **basic**, create a client object by using your (or any other matrix42 CMBD) account:

```{python}
import matrix42sdk
from matrix42sdk import AuthNClient
from matrix42sdk.api_endpoints import matrix42_objects, matrix42_fragments
```

For using Access/API Token, you can either set your MATRIX42SDK_API_TOKEN via a shell (**higher priority**):

```{shell}
export MATRIX42_URL="xxx"
export MATRIX42SDK_API_TOKEN="xxx"
```
and then:

```{python3}
mat = matrix42_fragments.GDSFragements()
```

Then to [get a fragment for a specific CI](https://help.matrix42.com/030_DWP/030_INT/Business_Processes_and_API_Integrations/Public_API_reference_documentation/Fragments_Data_Service%3A_Get_Fragment_data), insert correct parameters according to the documentation:

```
JUPYTERLAB_ID_FRAG = "8c51cfff-bf16-452e-8d2c-527cc25518c3"
SYS_ENTITY = "SPSSoftwareType"
full_ci_frg = mat.get_fragement(SYS_FRAGEMENT, JUPYTERLAB_ID_FRAG)
```

# What works and what does not?

Works:

- get and put (i.e. update) fragment

Use Cases:

- updating CI version numbers

Semi/or not working:

- creating fragment was not tested, but is implemented as a Rest API call
- get and put object -> here not tested extensively and one must expect bugs


# Testing

Without having a Matrix42 ESM portal which allows API access and is publicly available for unlimited use, the only option how to test this library is
to use **your** own ESM portal installation (be it in public cloud or on prem).
Hence the need to use your own API keys, etc.

From this follows that this library cannot - as of now - include more python tests, at least not publicly available.
It is my recommendation to write your `own, private tests` and report issues here.

Sorry for inconvenience!

## Python 3 - Simple Testing

Using `requests` you can call

```
import requests

url = "https://xxxx/m42Services/api/ApiToken/GenerateAccessTokenFromApiToken/"

payload = {}
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer the 'short' version of bearer token generated from Administration Panel in the GUI'
}

response = requests.request("POST", url, headers=headers, data = payload, verify = False)

print(response.text.encode('utf8'))

# only then start using proper API requests
import requests

url = "https://xxxx/m42Services/api/data/fragments/Ud_SoftwareproduktVersionClassBase/775c82cf-d243-4bfb-a1b2-f3edad93c826"

payload = {}
headers = {
  'Authorization': 'Bearer "output of the previous requests "RawToken" '
}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
```

# Building this package yourself

This package is being build on Azure DevOps services:

<https://dev.azure.com/johnmalc/Matrix42SDK/_build>

and further uses SonarCloud:

<https://sonarcloud.io/dashboard?id=dmpe_matrix42sdk>

Use to install package from non-PyPI feed (the azure one):

```
pip3 install --index https://pkgs.dev.azure.com/johnmalc/Matrix42SDK/_packaging/my-feed/pypi/simple/ matrix42sdk
```
