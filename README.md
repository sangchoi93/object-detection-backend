# Object Detection Flask REST API

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

## TODO:
1. API Swagger for proper rest documentations
2. Missing created datetime for each object
3. Different algorithms to detect object
4. Aggregate scores by averaging different detection algorithms
5. If there are multiple labels, take filename into account to pick one object over another?
6. Compress image contents
7. Explore more cost effective data store to preserve image contents instead of sql database
8. Determine if file/url provided is an image.