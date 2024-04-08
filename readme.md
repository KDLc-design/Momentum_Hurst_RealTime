# Dash Application Project

This project is a Dash application for real-time FX trading using Oanda API & customized strategy (Momentum, Hurst & RSI). It includes backtesting & real-time trading functionalities.

## Table of Contents

- [Dash Application Project](#dash-application-project)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
  - [Disclaimer](#disclaimer)

## Project Structure

Here's a high-level overview of the directory structure:

```plaintext
.
├── assets       # Contains static files like css and js files.
├── components   # Components used in Dash app.
    └── common     # Skeleton components used across components
├── configs      # Configuration files and constants for app & Oanda.
├── services     # Service modules for handling data retrieval & processing.
└── app.py       # The main entry point of the Dash application.
```

## Getting Started
Install all required packages before running:\
`pip install requirements.txt`\
Run local Dash server:\
`python app.py` or `python3 app.py`.\
Access the application via http://localhost:8050. You may customize server configurations under `./configs/server_conf.py`.

## Disclaimer

This project is created for educational purposes as part of the FT5010 group project at the National University of Singapore (NUS) and is not intended to provide investment advice.