# haplohub.PredictionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_prediction**](PredictionsApi.md#get_prediction) | **GET** /api/v1/predictions/{prediction_id}/ | Get prediction
[**get_prediction_results**](PredictionsApi.md#get_prediction_results) | **GET** /api/v1/predictions/{prediction_id}/results/ | Get prediction results
[**list_predictions**](PredictionsApi.md#list_predictions) | **GET** /api/v1/predictions/ | List predictions
[**run_prediction**](PredictionsApi.md#run_prediction) | **POST** /api/v1/predictions/ | Run prediction


# **get_prediction**
> Response2 get_prediction(prediction_id)

Get prediction

Get prediction by its ID

### Example

* Bearer Authentication (ApiAuthBearer):
```python
import time
import os
import haplohub
from haplohub.models.response2 import Response2
from haplohub.rest import ApiException
from pprint import pprint

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: 
configuration = haplohub.Configuration(
    access_token=os.environ["API_KEY"]
)

# Enter a context with an instance of the API client
with haplohub.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = haplohub.PredictionsApi(api_client)
    prediction_id = 'prediction_id_example' # str | 

    try:
        # Get prediction
        api_response = api_instance.get_prediction(prediction_id)
        print("The response of PredictionsApi->get_prediction:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PredictionsApi->get_prediction: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prediction_id** | **str**|  | 

### Return type

[**Response2**](Response2.md)

### Authorization

[ApiAuthBearer](../README.md#ApiAuthBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_prediction_results**
> Response3 get_prediction_results(prediction_id)

Get prediction results

Get prediction results by prediction ID

### Example

* Bearer Authentication (ApiAuthBearer):
```python
import time
import os
import haplohub
from haplohub.models.response3 import Response3
from haplohub.rest import ApiException
from pprint import pprint

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: 
configuration = haplohub.Configuration(
    access_token=os.environ["API_KEY"]
)

# Enter a context with an instance of the API client
with haplohub.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = haplohub.PredictionsApi(api_client)
    prediction_id = 'prediction_id_example' # str | 

    try:
        # Get prediction results
        api_response = api_instance.get_prediction_results(prediction_id)
        print("The response of PredictionsApi->get_prediction_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PredictionsApi->get_prediction_results: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prediction_id** | **str**|  | 

### Return type

[**Response3**](Response3.md)

### Authorization

[ApiAuthBearer](../README.md#ApiAuthBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_predictions**
> PaginatedResponsePredictionSchema list_predictions()

List predictions

List all predictions

### Example

* Bearer Authentication (ApiAuthBearer):
```python
import time
import os
import haplohub
from haplohub.models.paginated_response_prediction_schema import PaginatedResponsePredictionSchema
from haplohub.rest import ApiException
from pprint import pprint

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: 
configuration = haplohub.Configuration(
    access_token=os.environ["API_KEY"]
)

# Enter a context with an instance of the API client
with haplohub.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = haplohub.PredictionsApi(api_client)

    try:
        # List predictions
        api_response = api_instance.list_predictions()
        print("The response of PredictionsApi->list_predictions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PredictionsApi->list_predictions: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**PaginatedResponsePredictionSchema**](PaginatedResponsePredictionSchema.md)

### Authorization

[ApiAuthBearer](../README.md#ApiAuthBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **run_prediction**
> Response1 run_prediction(run_prediction_request)

Run prediction

Run a new prediction by specified version and model ID

### Example

* Bearer Authentication (ApiAuthBearer):
```python
import time
import os
import haplohub
from haplohub.models.response1 import Response1
from haplohub.models.run_prediction_request import RunPredictionRequest
from haplohub.rest import ApiException
from pprint import pprint

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: 
configuration = haplohub.Configuration(
    access_token=os.environ["API_KEY"]
)

# Enter a context with an instance of the API client
with haplohub.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = haplohub.PredictionsApi(api_client)
    run_prediction_request = haplohub.RunPredictionRequest() # RunPredictionRequest | 

    try:
        # Run prediction
        api_response = api_instance.run_prediction(run_prediction_request)
        print("The response of PredictionsApi->run_prediction:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PredictionsApi->run_prediction: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_prediction_request** | [**RunPredictionRequest**](RunPredictionRequest.md)|  | 

### Return type

[**Response1**](Response1.md)

### Authorization

[ApiAuthBearer](../README.md#ApiAuthBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

