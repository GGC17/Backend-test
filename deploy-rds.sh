#!/bin/bash
cd ./terraform
terraform init &&
terraform apply -var-file="secret.tfvars"
