
# This project was developed in a DevOps class at Texas A&M University, involving a team of six people. Throughout its progression, the project encompassed various phases. The core component is a versatile REST API capable of multiple tasks, with its primary functions encompassing log file parsing, Slack channel interaction for value submission, and the management of key-value pairs within a Redis database. Validation and verification were ensured through comprehensive testing using the test_api.py script, which assessed each endpoint of the API code. The project reached its deployment stage by hosting the API on a Flask server within a Docker container, an environment that was transitioned onto Google Cloud Platform (GCP). The workflow is further streamlined by implementing a GitHub Actions Workflow, which automatically tests and deploys each part of this process. 


## Below is some information we kept in the README throughout the span of this project
Please import Python libraries requests and pytest.
After running our API, the test can be run by the following command: py -m pytest test_api.py

---

Files located in folder project6. Docker Hub repository: andersoncolleen/project6:part2

Link to Docker image: https://hub.docker.com/r/andersoncolleen/project6 (tag: part2)

---


Please note this program requires the following;
1. pip
2. python
3. Flask

The program can be run by 'flask --app main.py run' within the Flask virtual environment (venv).

---
