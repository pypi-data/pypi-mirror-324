# langchain-jenkins

This package contains the LangChain integration with Jenkins

## Installation

```bash
pip install -U langchain-jenkins
```

And you should configure credentials by setting the following environment variables:

* TODO: fill this out

## Tools

`ChatJenkins` class exposes chat models from Jenkins.

```python
from langchain_community.tools.jenkins.tool import JenkinsJobRun
from langchain_community.utilities.jenkins import JenkinsAPIWrapper

tools = [
    JenkinsJobRun(
        api_wrapper=JenkinsAPIWrapper(
            jenkins_server="https://example.com",
            username="admin",
            password=os.environ["PASSWORD"],
        )
    )
]


jenkins_job_content = ""
src_file = "job1.xml"
with open(src_file) as fread:
    jenkins_job_content = fread.read()
tools[0].invoke({"job": "job01", "config_xml": jenkins_job_content, "action": "create"})
```
