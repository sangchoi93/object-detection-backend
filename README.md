# Object Detection Flask REST API
## TODO:
1. api swagger for proper rest documentations
2. missing created datetime for each object
3. different algorithms to detect object
4. aggregate scores by averaging different algorithms
5. If there are multiple labels, take filename into account to pick one object over another?
6. compress content
7. use nosql to store image contents

## Before running the app
1. Create Cloud Vision account and API key by following steps here:
https://cloud.google.com/vision/docs/before-you-begin

You must download your api key file in json format somewhere in your workspace for the next step.

2. Setup a virtual env with requirements.txt
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to run app
```
python3 -m app -c <path_to_api_key_json>
```

## How to run tests
```
python3 -m pytest
```