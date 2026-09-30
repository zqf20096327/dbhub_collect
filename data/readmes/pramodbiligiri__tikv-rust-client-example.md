Overview
========
This project does a basic demo of the tikv Rust client. The Rust client connects to a 
tikv server and stores and retrieves a value from it. Three different Docker containers are
used in this example:
1. The tikv Rust client
1. The tikv server
1. The tikv Placement Driver

This project is based on the documentation in the "Create New Project" section at 
https://tikv.org/docs/4.0/tasks/try/docker-stack/

Prerequisites
-----------
* Clone the [client-rust](https://github.com/tikv/client-rust) project of tikv into a sibling folder of this project. That is,
if this project is in a `workspace` folder, the folder structure should look like this:  
```  
$ ls workspace/  
    tikv-rust-client-example  
    client-rust
```  
You can use the following command to clone client-rust  
$ git clone https://github.com/tikv/client-rust.git  
  
* You need root permission to do the bind mount needed to build the Docker image

Build the docker image
---------------------
If this is the first time you are running this project, build the docker image:  
$ mkdir client-rust  
$ sudo mount --bind ../client-rust client-rust # Or su as root and do the same  
$ ./build-docker-image.sh  
$ docker image ls # Output should include the bitken/tikv-example image

How to run
-----------
Make sure the Docker image for this example has been built, as per instructions above

\# Start the tikv server application  
$ docker stack deploy --compose-file stack.yaml tikv  

\# Check if its components are running  
$ docker service ls # output should look like below  
```
ID                  NAME                MODE                REPLICAS            IMAGE                 PORTS
1ftb7p7rmrlm        tikv_pd             replicated          0/1                 pingcap/pd:latest     *:2379-2380->2379-2380/tcp
uxdyhqz45zvz        tikv_tikv           replicated          1/1                 pingcap/tikv:latest   *:20160->20160/tc
```
\# Start the tikv-example container with an interactive shell  
$ ./start-docker.sh  
  
\# Inside the tikv-example container:  
$ cd /home/tikv/tikv-example  
$ ./target/release/tikv-example  
Displays some sample output if interaction with tikv was successful  
  
\# To stop
\# Inside the tikv-example container  
$ exit  
\# To stop the tikv server application    
$ docker service scale tikv_pd=0 tikv_tikv=0  
  
\# To start again  
$ docker service scale tikv_pd=1 tikv_tikv=1  
  
\# To check metrics  
$ docker run --rm -ti --network tikv alpine sh -c "apk add curl; curl http://pd.tikv:2379/metrics"  
\# A lot of output...  
$ docker run --rm -ti --network tikv alpine sh -c "apk add curl; curl http://tikv.tikv:20180/metrics"  
\# A lot of output...  
  
