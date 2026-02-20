# MODAL-backend
Backend for the MODAL project

## Docker

### Build the image
docker build -t archive-browser .

### Run the container
docker run -p 8501:8501 archive-browser

#### Access at http://localhost:8501

## Installing venv
On mac/linux:
https://gist.github.com/pandafulmanda/730a9355e088a9970b18275cb9eadef3

## Using venv
Link with some info:
https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#

Create a virtual environment: 

```bash
python3 -m venv .venv
```

Activate a virtual environment:

```bash
source .venv/bin/activate
```