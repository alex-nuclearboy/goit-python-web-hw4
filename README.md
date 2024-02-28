# GoIT Python Web Application

This repository contains a simple Python web application. 
The application includes a basic HTTP server that responds to GET and POST requests, along with a socket server for handling data transmission.

## Features

- HTTP server handling GET and POST requests
- Static file serving (HTML, CSS, logo image)
- Data submission via POST requests and storage in JSON format
- Socket server for additional data processing

## Prerequisites

 - Docker installed on the machine

## Getting Started

    # Сlone this repository to the local machine:
    $ git clone https://github.com/alex-nuclearboy/goit-python-web-hw4.git
    # Navigate to the cloned directory:
    $ cd goit-python-web-hw4
    # Build the Docker image:
    $ docker build -t python-web-app .
    # Run the container with external data storage:
    $ docker run -d -p 3000:3000 --name running-app -v $(PWD)/storage:/app/storage python-web-app
    # To stop and remove the running container, use the following commands:
    $ docker stop running-app
    $ docker rm running-app
