# haplohub.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**status**](DefaultApi.md#status) | **GET** /api/v1/status/ | Status


# **status**
> Response status()

Status

### Example

```python
import time
import os
import haplohub
from haplohub.models.response import Response
from haplohub.rest import ApiException
from pprint import pprint


# Enter a context with an instance of the API client
with haplohub.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = haplohub.DefaultApi(api_client)

    try:
        # Status
        api_response = api_instance.status()
        print("The response of DefaultApi->status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->status: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**Response**](Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

