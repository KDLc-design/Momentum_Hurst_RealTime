# Backtester (DEPRECATED)

This is the branch for backtester. It visualizes backtesting performance on MAANG stocks.

## Table of Contents

- [Backtester (DEPRECATED)](#backtester-deprecated)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
  - [Disclaimer](#disclaimer)

## Project Structure

Here's a high-level overview of the directory structure:

```plaintext
.
├── assets        # Contains static files like css and js files.
└── app.py        # The main entry point of the Dash application.
```

## Getting Started
Install all required packages before running:\
`pip install requirements.txt`\
Run local Dash server:\
`python app.py` or `python3 app.py`.\
Access the application via http://localhost:8050. You may customize server configurations under `./configs/server_conf.py`.

## Disclaimer

This project is created for educational purposes as part of the FT5010 group project at the National University of Singapore (NUS) and is not intended to provide investment advice.