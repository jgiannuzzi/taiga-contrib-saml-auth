#!/bin/sh

docker build -t taiga-contrib-saml-auth-build . && docker run --rm -ti -v $PWD/dist:/data/dist taiga-contrib-saml-auth-build
