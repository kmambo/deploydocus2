## Motivation behind `deploydocus`

### TLDR

1. Kubernetes offers great flexibility because it seeks to be all things for every
   application. It needs structure
   imposed upon it to actually make it useful.
2. `deploydocus` imposes structure upon containerized applications.
    1. It imposes best practices on application developers.
    2. It encourages "convention over configuration" to reduce the number of decisions
       that a
    3. In exceptional cases, where deviations from convention is need, `deploydocus`
       enables that as well.
3. Ditch YAML. Offer a Pythonic alternative.
4. Continuos delivery (CD) by a scripted-Python that can run in virtual machines (VMs),
   in a Kubernetes cluster a(yes, I
   know that is a bit meta!) as a `Job` or `CronJob` or in a serverless environment such
   as [Knative](https://knative.dev/docs/), [AWS Lambda](https://aws.amazon.com/lambda/), [Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview)

<!--`deploydocus` uses an open-source library [kubernetes-asyncio-pydantic](https://github.com/kmambo/kubernetes-pydantic-asyncio-client) that provides Python classes that stand-in for -->

### Why `deploydocus`?

_... or how does it ease the Kubernetes pain for application developers?_

It's probably easier if I [demonstrate with an example](example/webapp.md). The current
version of `deploydocus` comes with a ready-made Python class for deploying a standard  
web application. The web application I want to deploy is containerized and can be pulled
using docker.

#### The example container

```shell
# You can pull this container down to your local machine using
docker pull docker.io/pbhowmic/python-jsonserver:0.2
```

??? "The Simple Webserver code"
    ```python
    import logging.config
    import os
    from datetime import datetime, timezone
    from typing import Any, cast

    from dotenv import load_dotenv
    from fastapi import FastAPI, Request, status
    from fastapi.responses import JSONResponse

    # Configuration for logging
    CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format": "[%(levelname)-8s] - %(module)s:%(lineno)d - %(message)s"}
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "stderr": {
                "class": "logging.StreamHandler",
                "level": "ERROR",
                "formatter": "simple",
                "stream": "ext://sys.stderr",
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": [
                "stderr",
                "stdout",
            ],
        },
    }

    # Apply logging configuration
    logging.config.dictConfig(CONFIG)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Load environment variables
    load_dotenv(dotenv_path="/var/lib/www/.env")
    port: int = int(cast(str, os.getenv("HTTP_PORT", "8080")))
    ip_addr: str = cast(str, os.getenv("HTTP_ADDR", "0.0.0.0"))

    # Create FastAPI app
    app = FastAPI()


    # Define routes
    @app.get("/")
    async def root():
        """
        Root endpoint, returns current datetime, status, port, and IP address.
        """
        return {
            "datetime": datetime.now(tz=timezone.utc).isoformat(),
            "status": "OK",
            "port": port,
            "ip_addr": ip_addr,
        }


    @app.get("/livez")
    async def livez():
        """
        Liveness probe endpoint.
        """
        return {"path": "/livez", "status": "OK"}


    @app.get("/readyz")
    async def readyz():
        """
        Readiness probe endpoint.
        """
        return {"path": "/readyz", "status": "OK"}


    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: Any):
        """
        Handles 404 Not Found errors.
        """
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Not found"},
        )


    # Main entry point for running the server
    if __name__ == "__main__":
        import uvicorn

        uvicorn.run(app, host=ip_addr, port=port)

    ```

```shell
# And to run this (exposing the container port 8080 to the host;s port 8080)
docker run --rm -p 8080:8080 --name python-jsonserver-0.1.0 -d \
  docker.io/pbhowmic/python-jsonserver:0.1.0
```

```shell
# later, you can delete this running container using
docker container stop python-jsonserver-0.1.0
```

This is a standard webserver that exposes just the base URL `'/'` which when called
with an HTTP application using `curl`

```shell
$ curl -v localhost:8080 # returns the following on screen

* Host localhost:8080 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8080...
* connect to ::1 port 8080 from ::1 port 49626 failed: Connection refused
*   Trying 127.0.0.1:8080...
* Connected to localhost (127.0.0.1) port 8080
* using HTTP/1.x
> GET / HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/8.15.0
> Accept: */*
> 
* Request completely sent off
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Server: SimpleHTTP/0.6 Python/3.13.7
< Date: Sun, 24 Aug 2025 15:57:32 GMT
< Content-Type: application/json
< 
* shutting down connection #0
{"datetime": "2025-08-24T15:57:32.797775+00:00", "status": "OK", "port": 8080, "ip_addr": "0.0.0.0"}
```

calling the `/livez`  (or the `/readyz`) endpoints

```shell
$ curl -v localhost:8080/livez # returns the following on screen

* Host localhost:8080 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8080...
* connect to ::1 port 8080 from ::1 port 49664 failed: Connection refused
*   Trying 127.0.0.1:8080...
* Connected to localhost (127.0.0.1) port 8080
* using HTTP/1.x
> GET /livez HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/8.15.0
> Accept: */*
> 
* Request completely sent off
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Server: SimpleHTTP/0.6 Python/3.13.7
< Date: Sun, 24 Aug 2025 16:02:07 GMT
< Content-Type: application/json
< 
* shutting down connection #0
{"path": "/livez"}
```

Any other endpoint is unrecognized and it returns a 404 error

```shell
$ curl -v localhost:8080/api   

* Host localhost:8080 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8080...
* connect to ::1 port 8080 from ::1 port 49927 failed: Connection refused
*   Trying 127.0.0.1:8080...
* Connected to localhost (127.0.0.1) port 8080
* using HTTP/1.x
> GET /api HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/8.15.0
> Accept: */*
> 
* Request completely sent off
* HTTP 1.0, assume close after body
< HTTP/1.0 404 Not Found
< Server: SimpleHTTP/0.6 Python/3.13.7
< Date: Sun, 24 Aug 2025 16:09:03 GMT
< Content-Type: application/json
< 
* shutting down connection #0
{"error": "Not found"}
```

I want 3 instances of this running in the cluster. Every container will have HTTP
requests routed to it, taking turns. This way the load is shared amongst the 3 container
instances.
In Kubernetes speak, we are running a single _Deployment_ with 3 _Replicas_ which
creates 3 _Pods_, each _Pod_ is running the `python-jsonserver` container (Pod is
really an abstraction for a container running on compute node such as a virtual
machine).
