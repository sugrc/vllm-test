# Realism evaluation system for synthetic images
This program checks whether a synthetic image is realistic enough.

## Table of Contents
1. Description
2. Getting started
    - Prerrequisites
        * Software
        * Hardware
    - Installation
4. Usage
5. Documentation
6. API documentation
7. Testing
8. Roadmap
9. Contribution
10. License


## Description
This project evaluates if a synthetic image is realistic enough using VQA.

## Getting Started

### Prerequisites

#### Software
- Python 3.12
- vLLM
- Docker and Docker compose
- Linux or WSL

#### Hardware
- 24GB RAM
- 1GB GPU RAM (VLM SmolVLM-256M)

### Installation
1. Clone this repository
2. In a Linux terminal, run \Docker compose up --build\''


## Usage
In the directory where the docker-compose.yaml file is located, run \docker compose up --build\''.
It's recommended to run \docker compose down\'' after usage.

## Documentation
This program was implemented based on the paper REAL: Realism Evaluation of Text-to-Image Generation Models for Effective Data Augmentation which can be found in the next link: https://arxiv.org/abs/2502.10663#:~:text=To%20address%20this%20gap%2C%20we%20propose%20REAL%2C%20an,visual%20attributes%2C%20unusual%20visual%20relationships%2C%20and%20visual%20styles. 

## API documentation


## Testing
This project includes one unit test to verify the correctness of a function. This test is implemented using PyTest.

## Roadmap


## Contribution


## License
