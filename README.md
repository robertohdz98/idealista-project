# IDEALISTA Rent Price Predictor

IDEALISTA Rent Price Predictor is a POC of an entire ML project.

## Description

- **ETL pipelines** using Apache Airflow
- **Database storage** using PostgreSQL
- **ML experiments**
- **Model serving** using FastAPI

This is a Python-based project. All components are containerised using Docker.

## Table of contents

    ├── .devcontainer
    ├── deployment                   <--- Entire stack deployment files
    │     ├── docker-compose/
    │     └── kubernetes/
    │
    ├── svc-***
    │   ├── docs/                    <--- Docs for indiv component
    │   ├── src/                     <--- Source code for indiv component
    │   │   ├── modules/
    │   │   └── app.py
    │   ├── tests/                   <--- Tests for indiv component (if needed)
    |   ├── Dockerfile               <--- Dockerfile for indiv component (if needed)
    │   ├── poetry.lock              <--- Poetry dependencies (do not edit)
    │   └── pyproject.toml           <--- Component dependencies management
    │
    ├── .gitignore
    ├── dev.Dockerfile               <--- Dockerfile for dev environment
    ├── poetry.lock                  <--- Poetry dependencies (do not edit)
    ├── pyproject.toml               <--- dev dependencies management
    └── README.md                    <--- Top-level description of the project

## Getting Started

### Dependencies

General dependencies and libraries in the entire monorepo are managed by Poetry, using
*poetry.lock* and *pyproject.toml* files of root directory.

Individual components/services include their own dependency files to manage their
own environment and libraries, excluding the ones that are not needed for isolation.

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

## Authors

- Roberto Hernández Ruiz
- Jorge Tarancón

## License


## Acknowledgments
