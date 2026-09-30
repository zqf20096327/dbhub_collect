# DM848-project

After some discussion and drawing on a board(30 November), we have defined what we think that the program should do.

## Version 1:
This is the version thats running and working in the cloud right now (30 nov).
- A deployment is running in the kubernetes cluster, called **jolie-deployer**. This has 1 replica and exposes port 8080. The image that it is running, is `joelhandig/cloud_server`. This image exposes the `cloud_server_iface`, where you can load or unload a service.
- A service is running in the kubernetes cluster, also called **jolie-deployer**. It exposes ports 8000 and 8080, and redirects to the deployment. It runs in external IP 35.228.66.168. Both the `.yaml` files used to create these objects, are found in the github repo in the `kubernetes/` folder.

This is what it can do:
- A user can supply a jolie program to `35.228.66.168:8000`. The user will get a token in return. 
- After that, the user can call the program on `35.228.66.168:8080`.
- A user can unload the program using the token gotten when loaded.

The problem with this approach are the following:
1. Only user programs that use port 8080 can be used. Everything else will load, but only 8080 will be exposed.
2. Only one program that use port 8080 can be loaded. The server will reject another program, saying that the port is already in use.

## Version 2
This is the one that we are building from now on (30 nov)
* A program is run (somewhere), call it **jolie-creator**. This somewhere is a place that is authenticated against the google cloud account, and has `kubectl` installed. The program needs to be able to be accessed by a user of our system. The current idea is to implement this in Java, and embed it in a jolie program, so it can be accessed from outside the system. We are not sure yet, if we should run it in the cluster, or on the Virtual Machine that is connected to the google account. This program takes a **manifest** and a **user_jolie_program** as an input, and does the following:
    1. `deployment.yaml`: Defines the amount of replicas that the user wants. Expose port 8000
    2. `service.yaml`: Defines what ports the user wants + port 8000. The image used should be the Dockerfile described later in this list.
    3. Saves the **user_jolie_program** to the disc to some standard location.
    4. Call `kubectl create -f deployment.yaml` and `kubectl create -f service.yaml`. This creates the whole service that the user asked for.
    5. Gets the IP address for the newly deployed jolie program. This could be gotten with `kubectl get services` some way. Returns this IP to the user.
* The Dockerfile should be like the one from version 1, but in the `CMD` section, which is the command run when the image is run somewhere, should also embed the **user_jolie_program** when it starts up.

Problems that we have not solved yet are:
* If the user wants more then one replica, the deployment will be replicated. If we then load the jolie program in that deployment, we are not sure of which of the replicas the load balancer will choose, and it will only chose one of them. If the user tries to use the service, and is directed to a replica that does not have the jolie program loaded, then there will be a problem. This is why we need to embed the program when the docker image is started, but the docker image does not have access to that program.
    * Possible solution: The **jolie-creator** offers a way of retrieving a jolie program, that the dockerfile can call to get the program. Possible security hole here?


## Version 3:
* The **Jolie-deployer** is running as a jolie program in the google cloud. It is authenticated against the cluster and can run `kubectl` commands. The program listens to users that wants to deploy a service. The interactions happen like this:
1. User tells **jolie-deployer** that it wants to load a new service. It tells it what ports to use, name of service, number of replicas along with the program and some other data.
2. The **jolie-deployer** generates a new token for this service. Writes the file to disk, using `<token>.ol` as filename. Writes `deployment.yaml` and `service.yaml` to disc after the user specification. NOTE `imagePullPolicy: Always`. Also note that the token is set as an enviroment variable in the new deployment. This `deployment.yaml` uses **cloud_server** as it's image.
3. **jolie-deployer** starts up the new service and deployment.
4. Upon startup, the **cloud_server** asks **jolie-deployer** what program it should run, querying with the token.
5. **jolie-deployer** reads from disc with the filename specified. Returns the program.
6. **cloud_server** embeds and runs the user jolie-program.

This is done so that when a user wants several replicas, the program is embedded in all of them.

The user based health check can be submitted with setting `healthcheck = true` in the `userloadrequest`. The health check must listen on **localhost:4001/health**, and if it returns anything else but `true`, then the pod is considered unhealthy.