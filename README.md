# busin-server-fastapi

## Table of Contents

- [busin-server-fastapi](#busin-server-fastapi)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)

## About

This is a simple server made with FastAPI to be used with the [busin-app](https://github.com/omar-chaar/busin-app) project.

## Prerequisites

- Python 3.9+
- pip

## Installation

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt`
3. Create a config.py file with the following settings:

```python
URL_DATABASE = mysql+pymysql://user:password@localhost/dbname
SECRET_KEY = "verysecretkey"
ALGORITHM = "HS256"
```

## Usage

1. Run the server with `python main.py`

## License

Distributed under the GNU GPLv3 License. See `LICENSE` for more information.
