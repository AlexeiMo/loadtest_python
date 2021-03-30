# Load Testing

Load testing using Locust framework for "https://34.91.47.190"


## Key Features
- Tests are written in Python (locust)

## Repo Layout

- loadtest_python/data - stored files which is used in requests.
- loadtest_python/test_locust.py - load test scenarios which
  can be run on locust
- loadtest_python/helpers - different utilities used in tests
  (e.g. asserting response status code)

## Config
- loadtest_python/docker-compose.yaml - configuration file for Docker
  distributed running
- loadtest_python/target.json - data used in tests (e.g. user credentials,
  URLs for API requests)


## Usage

### Install/Build
Run commands in the terminal IDE:
1. Install python3
2. python3 -m venv env (create env)
3. cd env\\Scripts (go to env activation folder)
4. activate.bat (activate env)
5. pip install locust (install Locust framework dependencies)


### Run Project Tests (Locally)
Run commands in the terminal IDE:
1. locust -f test_locust.py --headless -u 20 -r 1 -t 60s --only-summary

### Run Project Tests (Docker Container)
Run commands in the terminal IDE:
1. docker-compose up --scale worker=4
2. Open browser and type "http://localhost:8089/"
3. Type test options you want (total users number and spawn rate)
4. Press "Start swarming"
5. Press "Stop" if you want to stop test process

#### target.json
Requires valid email/password in "target.json" for valid login
process (required quite for all tests)
```json
{
  "user":{
    "login": {
      "email": "<user-login-email>",
      "password": "<user-login-password>"
    }
  },
  "admin": {
    "login": {
      "email": "<admin-login-email>",
      "password": "<admin-login-password>"
    }
  } 
}
```