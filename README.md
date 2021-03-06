# Kladama API for Python

![Master Build](https://github.com/plexilar/kladama-api-python/workflows/Build/badge.svg?branch=master)

Python API for Kladama Services Integration

## How to install it

You can install the API through PIP

```shell script
pip install kladama-api
```

## How to start using it. "List available Variables" example.

First, you must to authenticate through a <em>API Token</em> that must be provided to you. This authentication process returns a session object that must be used to create a `Context` object.

```python
# retrieve all available variables

import kladama as kld

env = kld.Environments().prod
api_token = '<your provided token>'
session = kld.authenticate(env, api_token)

query = kld.Queries().var

response = kld.Context(session).get(query)

if isinstance(response, kld.Success):

    for var in response.result:
        print(var.name, '-', var.description, 'in', var.link)
```

## How to check if a GeoJson data can be used as a valid AoI in Kladama

```python

import kladama as kld

env = kld.Environments().prod
api_token = '<your provided token>'
session = kld.authenticate(env, api_token)

query = kld.Services().validate_aoi({
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "id": "897d8348a539983c4f435b45",
                        "name": "field-1"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [-50.675417,-22.000000],
                                [-10.675394,-21.000000],
                                [-30.669532,-21.000000],
                                [-50.656133,-21.000000],
                                [-60.656118,-21.000000],
                                [-50.675417,-22.000000]
                            ]
                        ]
                    }
                }
            ]
        })

response = kld.Context(session).get(query)
if isinstance(response, kld.Error):
    print(response.__str__())
else:
    print('Valid: ', response.result['valid'])
    for message in response.result['messages']:
        print(message)
```

## How to add an area of interest (AoI)

```python

import kladama as kld

env = kld.Environments().prod
api_token = '<your provided token>'
session = kld.authenticate(env, api_token)

transaction = kld.Transactions()\
    .add_aoi\
    .for_user('<your user>')\
    .with_name('<aoi name>')\
    .with_description("Test AOI")\
    .with_category("Test")\
    .with_features({
        "type": "FeatureCollection",
        "name": "Test AoI",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "id": "897d8348a539983c4f435b45",
                    "name": "field-1"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-50.675417,-22.000000],
                            [-10.675394,-21.000000],
                            [-30.669532,-21.000000],
                            [-50.656133,-21.000000],
                            [-60.656118,-21.000000],
                            [-50.675417,-22.000000]
                        ]
                    ]
                }
            }
        ]
    })

response = kld.Context(session).execute(transaction)
if not isinstance(response, kld.Success):
    print(response.__str__())

# Also, you can add an AoI from a JSON file
transaction = kld.Transactions()\
    .add_aoi\
    .for_user('<your user>')\
    .with_name('<aoi name>')\
    .with_description("Test AOI")\
    .with_category("Test")\
    .from_file('<JSON filename>')
```

## How to create a Periodic Subscription to a variable

```python
# create periodic subscription

import kladama as kld

env = kld.Environments().prod
api_token = '<your provided token>'
session = kld.authenticate(env, api_token)

# could be any other Spatial Operation (MIN, MAX, STD, etc)
transaction = kld.Transactions()\
    .periodic_subsc\
    .for_user('<your user>')\
    .with_variable('<var name>')\
    .with_operation('MEAN')\
    .with_aoi('<aoi name>')

response = kld.Context(session).execute(transaction)

if isinstance(response, kld.Success):
    if response.type == kld.ResultType.OK:
        code = response.result['code'] # property 'code' contains ID of new created subscription
        print("New subscription code: ", code)
    else:
        print("Redirect to: ", response.result['href']) # property 'href' contains URI of identical subscription resource
else:
    print('Error code: ', response.code, 'Message: ', response.message)
 ```

## How to get last data from a periodic subscription

```python

import kladama as kld

env = kld.Environments().prod
api_token = '<your provided token>'
session = kld.authenticate(env, api_token)

query = kld.Queries()\
    .subsc\
    .by_user('<your user>')\
    .by_key('<subscription code>')\
    .results\
    .last

response = kld.Context(session).get(query)
if isinstance(response, kld.Error):
    print(response.__str__())
elif response.result is None:
    print('response is successful but empty')
else:
    assert isinstance(response.result, kld.BinaryResult)
    print('Saving to file: ', response.result.name)
    with open(response.result.name, mode='wb') as fh:
        fh.write(response.result.content)
```
