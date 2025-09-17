# Deploydocus

The cloud-native application deployment framework for developers.

## The Audience

### or for whom is this meant?

`deploydocus` (Python package name `deploydocus2`) is a framework to help application developers deploy their applications to Kubernetes clusters and maintain. It assumes the application developers know that their application will be containerized and then deployed to a Kubernetes cluster.

The containerized application could be a RESTful server or a node ina data pipeline (such as a long running database query)  or a Kafka consumer microservice etc. In Kubernetes parlance, the developers are building **workloads**. 

A spillover beneficiary will be Kubernetes operators who can use `deploydocus` to promote the application from a development environment to staging, user acceptance testing and all the way to production environments. 

### and who is not the target audience (yet)?

In its current incarnation, `deploydocus` is not meant to deploy control plane components such as controllers, custom resource definitions, create clusterwide Kubernetes objects (such as cluster roles, cluster role bindings, validating admission webhooks etc). 

I will get around to this eventually - and Kubernetes controller developers and operators deserve to have their lives be easier - but for now, my  focus needs to be developers, who should not have to have an extensive understanding of the beast that is Kubernetes, to develop and deploy their applications.
