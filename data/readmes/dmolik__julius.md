# Julius

A CalDav calendaring server implemented using [Go](https://golang.org), [github.com/samedi/caldav-go](https://github.com/samedi/caldav-go), and [Postgres](https://www.postgresql.org/) designed to be small and efficient.

## Building

To build Julius you will need Golang and a Make variant. Then, Simply run `make`.

### Dependencies

  - [Golang](https://golang.org)
  - [Make](https://www.gnu.org/software/make/)
  - [Docker](https://www.docker.com)

## Running

### Minikube (Kubernetes)

Start a local Kubernetes cluster using Minikube and then deploy Julius.

    make minikube
    make deploy
    export USER=<USER>
    export PASSWORD=<PASSWORD>
    make seed
    make tunnel # Optional, if you want to access Julius from your local machine, (route the load balancer to your local machine)

### Docker Compose

Start the containers locally and then add users manually, just replace `USER` and `PASSWORD` with your desired values.

    make up
    docker exec -it julius-db-1 psql -U julius julius -c "INSERT INTO users (username, email, password) VALUES ('USER', 'USER@julius.local', crypt('PASSWORD', gen_salt('bf', 12)));"
    docker exec -it julius-db-1 psql -U julius julius -c "INSERT INTO collections (owner_id, name) VALUES (1, '/');"
    docker exec -it julius-db-1 psql -U julius julius -c "INSERT INTO collection_roles (collection_id, user_id, permission) VALUES (1, 1, 'admin');"
