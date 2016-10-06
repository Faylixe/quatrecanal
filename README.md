# quatrecanal

A Giphy-like bot which pic random data from 4chan nsfw boards.

## Installation

Here is how to install and run this command in your slack team, using Docker :

```bash
git clone https://github.com/Faylixe/quatrecanal.git
cd quatrecanal
docker build -t quatrecanal .
docker run -e SLACK_WEBHOOK_TOKEN="your_team_token" -d -p 5000:5000 quatrecanal
```
