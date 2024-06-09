## OSINT Web App Backend
<img src="https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png"
     alt="Markdown Python icon"
     height="50px"
/>&nbsp;&nbsp;&nbsp;
<img src="https://cdn.worldvectorlogo.com/logos/fastapi.svg"
     alt="Markdown FastAPI icon"
     height="50px"
/>&nbsp;&nbsp;&nbsp;
<img src="https://img.icons8.com/fluency/48/000000/docker.png"
     height="50px"/></span>
&nbsp;&nbsp;&nbsp;

### Introduction

This is a backend app for osint web app.

### Usage

The app requires an `.env` file. You can copy content from `.env.example`:

To execute dependencies run in the terminal:

```
./init.sh 
```

### Running Using Docker

To build and run Docker container use the following command:

```
docker-compose down                                     
docker-compose up --build

```
For testing endpoints open `http://0.0.0.0:8000/docs` in the browser