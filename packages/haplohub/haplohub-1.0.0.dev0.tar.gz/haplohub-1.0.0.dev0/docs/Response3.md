# Response3


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**ResponseStatus**](ResponseStatus.md) |  | [optional] 
**result** | [**PredictionResultsSchema**](PredictionResultsSchema.md) |  | 
**error** | [**ErrorSchema**](ErrorSchema.md) |  | 

## Example

```python
from haplohub.models.response3 import Response3

# TODO update the JSON string below
json = "{}"
# create an instance of Response3 from a JSON string
response3_instance = Response3.from_json(json)
# print the JSON string representation of the object
print Response3.to_json()

# convert the object into a dict
response3_dict = response3_instance.to_dict()
# create an instance of Response3 from a dict
response3_from_dict = Response3.from_dict(response3_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


