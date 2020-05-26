# Kladama API for Python

![Master Build](https://github.com/plexilar/kladama-api-python/workflows/Build/badge.svg?branch=master)

Python API for Kladama Services Integration

## How to install it

You can install the API through PIP

```shell script
pip install kladama-api
```

## How to start using it

First, you must to authenticate through a <em>API Token</em> that must be provided to you. This authentication process returns a session object that must be used to create a `Context` object.

```python
# retrieve all available variables

import kladama as kld

env = kld.Environments().prod
api_token = '<your provided token>'
session = kld.authenticate(env, api_token)

query = kld.Query().var

variables = kld.Context(session).get(query)
for var in variables:
    print(var.name, '-', var.description, 'in', var.link)
```

## How to add an area of interest

```python
# create a periodic subscription

import kladama as kld

env = kld.Environments().prod
api_token = '<your provided token>'
session = kld.authenticate(env, api_token)

operation = kld.Operations()\
    .add_aoi\
    .for_user('<your user>')\
    .with_name('<aoi name>')\
    .with_description("Test AOI")\
    .with_category("Test")\
    .with_features({
        "type": "FeatureCollection",
        "name": "Test AoI",
        "features": {
            "type": "Feature",
            "properties": {
                "id": "5b8c9e286e63b329cf764c61",
                "name": "field-1",
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [-60.675417,-21.854207],
                                [-60.675394,-21.855348],
                                [-60.669532,-21.858799],
                                [-60.656133,-21.85887],
                                [-60.656118,-21.854208],
                                [-60.675417,-21.854207]
                            ]
                        ]
                    ]
                },
            }
        }
    })

response = kld.Context(session).execute(operation)
if not isinstance(response, kld.Success):
    print(response.__str__())
```

## How to check an AoI

```python
# create get subscription info

import kladama as kld

env = kld.Environments().prod
api_token = '<your provided token>'
session = kld.authenticate(env, api_token)

query = kld.Helpers\
            .check_aoi({
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {
                            "id": "5b8c9e286e63b329cf764c61",
                            "name": "Jerovia - D9"
                        },
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [
                                        -60.675417,
                                        -21.854207
                                    ],
                                    [
                                        -60.675394,
                                        -21.855348
                                    ],
                                    [
                                        -60.669532,
                                        -21.858799
                                    ],
                                    [
                                        -60.656133,
                                        -21.85887
                                    ],
                                    [
                                        -60.656118,
                                        -21.854208
                                    ],
                                    [
                                        -60.675417,
                                        -21.854207
                                    ]
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
    print('Valid: ', response['valid'])
    for message in response['messages']:
        print(message)
```


## How to subscribe to a variable

```python
# create a periodic subscription

import kladama as kld

env = kld.Environments().prod
api_token = '<your provided token>'
session = kld.authenticate(env, api_token)

operation = kld.Operations()\
    .periodic_subsc\
    .for_user('<your user>')\
    .with_variable('ecmwf-era5-2m-ar-max-temp')\
    .with_source('ECMWF')\
    .with_operation('mean')\
    .with_aoi('<aoi name>')

response = kld.Context(session).execute(operation)
if isinstance(response, kld.Success):
    code = response.result['code'] # the code is the id of the subscription
else:
    print(response.__str__())
```

## How to get data from a periodic subscription

```python
# create get subscription info

import base64 as b64
import kladama as kld

env = kld.Environments().prod
api_token = '<your provided token>'
session = kld.authenticate(env, api_token)

query = kld.Query()\
    .subsc\
    .by_user('<your user>')\
    .filter_by('<subscription code>')\
    .last

response = kld.Context(session).get(query)
if isinstance(response, kld.Error):
    print(response.__str__())
else:
    print('Name: ', response.name, ' Binary Content:\n', b64.b64encode(response.content).decode('utf-8'))
```
