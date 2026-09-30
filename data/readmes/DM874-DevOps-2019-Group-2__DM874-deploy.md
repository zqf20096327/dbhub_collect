# Continuous Integration & Continuous Deployment

For our CI/CD pipeline, we use TravisCI's free open-source plan. 

This repository contains a docker image which contains the Kubernetes tool `kubectl`, which is used for continuous deployment.
Additionally, some skeleton code for implementing CI/CD in a service is available in the folders `scripts/no_migrations` if the service does not use the database, or `scripts/with_migrations` if database is used by the service.

The required steps for setting up CI/CD for a new service is described in the `travis.yml` files inside `scripts` folder.
The `travis.yml` files should be renamed to `.travis.yml`, and placed in project root along with folders `ci_scripts` and `migrations` (if appropriate).

> Environment variables needed are described in the respective `travis.yml` files

## Regarding migrations

If migrations are used, it is important to edit the script `migrations.sh` and insert the name of the database used.
In the future, this should probably be changed such that it can be done through an environment variable.

## The pipeline

### Building & Tests

Since all of our services are docker images, we decided that any present tests should be run during building of the image.
This simplifies the TravisCI configuration drastically.

Any long-running tests should be present only in non-master branches.

### Publishing images

Once an image is built, we use dockerhub to publish the image, allowing kubernetes to pull it from there once the Kubernetes statefulsets have been updated with new image tags.

All images are tagged with the commit hash given through `$TRAVIS_COMMIT`, which helps kubernetes determine if it is running the correct image (as opposed to using `latest` or constant tag).

Since TravisCI creates a fresh container for each stage, building and publishing is bundled in a single stage.

### Updating Kubernetes Statefulsets

Once an image passes the `build-publish` stage, the deploy stage uses the `dm874/deploy` image built from this repository, to update the images in our kubernetes cluster.

## Secrets

We use travis secrets to store the following:

- docker username
- docker password
- kubernetes bearer token

these secrets should never be used in building, but rather in the ENTRYPOINT / CMD of docker images.

The secrets are generated with the TravisCI CLI tool/gem through `travis encrypt VARIABLE=VALUE`.
