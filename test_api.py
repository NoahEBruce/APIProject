#import Python libraries requests and pytest
#run API. For example: docker run -p 8000:4000 andersoncolleen/project6:part2
#in a new CMD prompt window, run the following command: py -m pytest test_api.py 

import requests
import pytest

test_data = [
    ("md5", "", 404, None),
    ("md5", "test", 200, "098f6bcd4621d373cade4e832627b4f6"),
    ("md5", "123", 200, "202cb962ac59075b964b07152d234b70"),
    ("md5", "hello%20world", 200, "5eb63bbbe01eeed093cb22bb8f5acdc3"),
    ("factorial", "", 404, None),
    ("factorial", "test", 404, None),
    ("factorial", 0, 200, 1),
    ("factorial", 1, 200, 1),
    ("factorial", 4, 200, 24),
    ("factorial", 5, 200, 120),
    ("fibonacci", "", 404, None),
    ("fibonacci", "test", 404, None),
    ("fibonacci", 1, 200, [0,1,1]),
    ("fibonacci", 8, 200, [0,1,1,2,3,5,8]),
    ("fibonacci", 60, 200, [0,1,1,2,3,5,8,13,21,34,55]),
    ("is-prime", "", 404, None),
    ("is-prime", "test", 404, None),
    ("is-prime", 0, 200, False),
    ("is-prime", 1, 200, False),
    ("is-prime", 2, 200, True),
    ("is-prime", 5, 200, True),
    ("is-prime", 10, 200, False),
    ("is-prime", 47, 200, True),
    ("slack-alert", "", 404, None),
    ("slack-alert", "test", 200, True),
    ("slack-alert", "hello%20world", 200, True)
    ]

@pytest.mark.parametrize("endpoint, input, expected_status_code, expected_output", test_data)
def test_api_get(endpoint, input, expected_status_code, expected_output):
    resp = requests.get(f"http://localhost:8000/{endpoint}/{input}")
    
    if resp.status_code == expected_status_code:
        try:
            #extract the JSON from HTTP results
            output = resp.json()['output']
        except:
            #unable to find 'output' key
            output = "Cannot read JSON payload."
        
        #Check tests for expected output
        if expected_output == None or output == expected_output:
            assert True
        else:
            assert output == expected_output,  "Found unexpected output: " + str(output) + ". Expected output: " + str(expected_output)
        
    else:
        #If the status code is unexpected
        assert resp.status_code == expected_status_code, "Found unexpected status code: " + str(resp.status_code) + ". Expected status code: " + str(expected_status_code)