# Problem Statement

Write a server which can generate random api keys, assign them for usage and release them after sometime. Following endpoints should be available on the server to interact with it.
1. There should be one endpoint to generate keys.
2. There should be an endpoint to get an available key. On hitting this endpoint server should serve a random key which is not already being used. This key should be blocked and should not be served again by E2, till it is in this state. If no eligible key is available then it should serve 404.
3. There should be an endpoint to unblock a key. Unblocked keys can be served via E2 again. 
4. There should be an endpoint to delete a key. Deleted keys should be purged. 
5. All keys are to be kept alive by clients calling this endpoint every 5 minutes. If a particular key has not received a keep alive in the last five minutes then it should be deleted and never used again.
# Problem Constraints
1. All blocked keys should get released automatically within 60 secs if point 3 is not called.
2. No endpoint call should result in an iteration of the whole set of keys i.e. no endpoint request should be O(n). They should either be O(lg n) or O(1).


# Requirements

 - Python>=3.5
 - Django=3.0.6
 - djangorestframework=3.11.0

## Project setup

Install requirements: (assuming python3 environment is activated)

    pip install -r requirements.txt

## endpoint to generate key

Here I am generating random API key with length 20. if key generated successfully it will return api_key with status code 201, and if duplicate key is generated then it will return a message that **key with this api key already exists** with status code 400 and won't save it into database. 

    http://127.0.0.1:8000/api/v1/random_api_key/
**Method** POST 
## endpoint to get an available key

Here I am returning an available key which is not being used (**An api key will be in use for 5 minutes from its last accessing time**) and starting  a **thread** to update key's last accessing time (**last accessing time is the time when we got the api key in response**) and blocking it.

    http://127.0.0.1:8000/api/v1/random_api_key/
   **Method** : GET

## endpoint to unblock a key

Here I am sending that api_key in **params** which we want to unblock.
It will unblock the key if key is existing and return response with status code **200** but if that key is not existing it will return a message **Kindly send key to be updated, given key does not exist** with status code **400**

    http://127.0.0.1:8000/api/v1/random_api_key/?api_key=5TRxfoyGQSLLkbiRoUPU
**Method** : PUT

## endpoint to delete a key

Here I am sending that api_key in **params** which we want to delete.
It will delete (hard delete) the key if key is existing and return response with status code **200** but if that key is not existing it will return a message **Kindly send key to be updated, given key does not exist** with status code **400**

    http://127.0.0.1:8000/api/v1/random_api_key/?api_key=5TRxfoyGQSLLkbiRoUPU

**Method** : DELETE

# Scheduler

Created a scheduler function which will be executed in every 60 seconds.
If any record found updated in last 60 second then it won't do anything but if any record not found updated in last 60 second then if will unblock all key's which are blocked.
To start scheduler we need to hit an API only once whenever server will be started or restarted.

    http://127.0.0.1:8000/api/v1/start_scheduler/

**Method** : GET
