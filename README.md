# Drip Haus Webscraper

## Overview
Drip Haus Webscraper is a Python script that connects to a WebSocket endpoint provided by the Drip Haus platform to fetch user data in real-time. The data collected is saved into an Excel file, allowing users to easily view and analyze the details of various Drip Haus profiles.

## Features
- Connects to a WebSocket server and fetches user data.
- Extracts information about users such as:
  - Creator Name
  - Profile URL
  - About Section
  - Number of Followers
  - Number of Thanks
  - Country
- Identifies country names from the user bio/description using regex and a predefined list of country names.
- Saves the extracted data to an Excel file for easy access and analysis.

## Requirements
The following Python libraries are required to run this project:

- `aiohttp` - Asynchronous HTTP client for Python, used to handle WebSocket connections.
- `requests` - Library to send HTTP requests.
- `pandas` - Data analysis library to handle data and save it into an Excel file.
- `json` - Standard library for handling JSON data.
- `re` - Regular expressions library used for matching country names.

To install the necessary libraries, you can use `pip`:
```bash
pip install aiohttp pandas requests
