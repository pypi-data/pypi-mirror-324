# langchain-jenkins

This package contains the LangChain integration with Jenkins

## Installation

```bash
pip install -U langchain-jenkins
```

And you should configure credentials by setting the following environment variables:
```bash
export JENKINS_SERVER="https://example.com"
export USERNAME="admin"
export PASSWORD=""
```

* TODO: fill this out

## Tools

`JenkinsJobRun` class exposes tool models from Jenkins.

```python
from langchain_jenkins import JenkinsAPIWrapper, JenkinsJobRun

tools = [
    JenkinsJobRun(
        api_wrapper=JenkinsAPIWrapper(
            jenkins_server="https://example.com",
            username="admin",
            password=os.environ["PASSWORD"],
        )
    )
]
```

### Create the Jenkins job
```python

jenkins_job_content = ""
src_file = "job1.xml"
with open(src_file) as fread:
    jenkins_job_content = fread.read()
tools[0].invoke({"job": "job01", "config_xml": jenkins_job_content, "action": "create"})
```


### Run the job
```python
tools[0].invoke({"job": "job01", "parameters": {}, "action": "run"})
```

### Get job status
```python
resp = tools[0].invoke({"job": "job01", "number": 1, "action": "status"})
if not resp["inProgress"]:
    print(resp["result"])
```

### Delete the job
```python
tools[0].invoke({"job": "job01", "action": "delete"})
```
