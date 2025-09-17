## Web application with `deploydocus2`

### The target deployment

![alt text](./cloud-deployment-Client_request_flow_through_Ingress_to_API_server_Pods.png)

### Pre-requisites

I assume you already have virtual environment created and `deploydocus2` installed <!-- TODO: link to pypi--> but if not, the following will do 

```shell
python3 -m venv .venv/example # create a new virtual environment
source .venv/example/bin/activate # activate the virtual environment
pip3 install deploydocus2
```

We are now ready for this script. 
I am going to use a bespoke container `python-jsonserver`

```python
from deploydocus2.components.workloads import SimpleHttpApplication
from deploydocus2.pkg import K8sModelSequence
from deploydocus2.utils import render

app_install = SimpleHttpApplication(
                app_name='httpserver',
                version="1.0.0",
                namespace="httpserver",
                app_image="docker.io/pbhowmic/python-jsonserver:0.2",
                app_ports={'http':8080}
            )

rendered: K8sModelSequence = app_install.gen_k8s_components().render() # returns a sequence of Kubernetes objects
print(render(rendered, 'yaml'))
```


