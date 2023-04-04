# Sushi
Multipurpose discord bot that uses Google Sheets as its databases. Spreadsheets must either be public or shared with the email generated in Google developer console.

Media responders will require a spreadsheet with embedable links or files to upload directly. Files cannot be larger than 8MB per Discord limitations.

### Built With
[`hikari`](https://github.com/hikari-py/hikari) - An opinionated, static typed Discord microframework for Python3 and asyncio that supports Discord's v10 REST and Gateway APIs.

[`Lightbulb`](https://github.com/tandemdude/hikari-lightbulb/) - An easy to use command handler library that integrates with the Discord API wrapper library for Python, Hikari.

[`miru`](https://github.com/HyperGH/hikari-miru) - An optional component handler for hikari, inspired by discord.py's views.

## Getting Started
- Python 3.9 or above
- Create a [Discord Application](https://discord.com/developers/applications)
- Create a [Google service account](https://console.cloud.google.com/) and project
- Create a [Twitter access token](https://developer.twitter.com/en/portal/dashboard)*

## Setup
- Create virtual environment: `python3 -m venv venv`
- Enter virtual environment: `source ./venv/bin/activate`
- Install dependencies: `pip3 install -r requirements.txt`

## Misc
There are two APIs that require access tokens to use, Google and Twitter. These tokens can either be hardcoded into the bot or added as enviornment variables. You will need to do some slight alteration to the code to add them as enviornment variable. 
