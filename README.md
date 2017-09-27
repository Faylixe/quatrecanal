# quatrecanal

A Giphy-like bot which pic random data from 4chan nsfw boards.

## Usage

quatrecanal is available directly on DockerHub, to run it just enter the following command :

```bash
docker run -e SLACK_WEBHOOK_TOKEN="your_team_token" -d -p 5000:5000 faylixe/quatrecanal
```

## Build

Here is how to install and run this command :

```bash
git clone https://github.com/Faylixe/quatrecanal.git
cd quatrecanal
docker build -t quatrecanal .
```
