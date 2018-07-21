#!/bin/bash

# Build and deploy on master branch
if [[ $CIRCLE_BRANCH == 'master' ]]; then
    echo "Connecting to docker hub"
    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

    echo "Building..."
    docker build -t gdude2002/ultros-site:latest -f docker/Dockerfile .

    echo "Pushing image to Docker Hub..."
    docker push gdude2002/ultros-site:latest
else
    echo "Skipping deploy"
fi
