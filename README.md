# Sushi
A multipurpose discord bot that uses [Supabase](https://supabase.com/dashboard/projects) as its database.

Files cannot be larger than 25MB per Discord limitations.

### Built With
[`hikari`](https://github.com/hikari-py/hikari) - An opinionated, static typed Discord microframework for Python3 and asyncio that supports Discord's v10 REST and Gateway APIs.

[`Lightbulb`](https://github.com/tandemdude/hikari-lightbulb/) - An easy to use command handler library that integrates with the Discord API wrapper library for Python, Hikari.

[`miru`](https://github.com/HyperGH/hikari-miru) - An optional component handler for hikari, inspired by discord.py's views.

## Getting Started
- Python 3.9 or above
- Create a [Discord Application](https://discord.com/developers/applications)
- Create a Supabase project

## Setup
- Create virtual environment: `python3 -m venv venv`
- Enter virtual environment: `source ./venv/bin/activate`
- Install dependencies: `pip3 install -r requirements.txt`

## Misc
The Supabase API requires a url and key token to use. This information can be hardcoded into the bot or added as enviornment variables. You must make slight alterations to the code to add them as enviornment variables. 

<img src="https://imgur.com/C3opkNz"/>
