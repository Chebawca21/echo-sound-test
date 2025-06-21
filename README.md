# echo-sound-test
Bot for discord imitating Echo / Sound Test from Skype

## Setup

### Making virtual environment
```
ptyhon3 -m venv venv
```

### Activating the environment
```
source venv/bin/activate
```

### Installing required packages
```
pip install -r requirements.txt
```

### Preparing the environment
Add `BOT_TOKEN` environment variable as shown in the example `.env` file and fill it with the token of your own bot.

To use this bot you also need to install FFMPEG and add it to your path. For linux systems it can be done with:
```
sudo add-apt-repository universe
sudo apt update
sudo apt install ffmpeg
```