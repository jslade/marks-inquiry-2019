# marks-inquiry-2019
Mark's Inquiry project for Lesher Middle School, spring 2019



## This = Test

this is america


### LEbron JAmes


## Setup

Install some dependencies

```bash
python3 -m pip install -U pygame --user
py -m pip install -U pubnub --user
py -m pip install -U colormath --user
py -m pip install -U mamba expects doublex doublex-expects --user
```

## How to Run It

```bash
py -m snake.main
```

## Running specs

```bash
python3 $(path_to_mamba) --format=documentation <spec paths>
```

On my linux system, `path_to_mamba` = `~/.local/bin/mamba` -- it will depend on how you have installed mamba


## The web app for multiplayer

The multiplayer mode uses [PubNub](https://pubnub.com/) to provide a "second-screen" controller experience:
* Run the game in multiplayer mode, which will connect the game to PubNub to receive remote player input
* Visit https://marks-inquiry-2019.herokuapp.com/ to load the multiplayer launcher.
* The launcher will display a QR code that players can scan on their phones to automatically join the game
* When players scan the QR code, they will be presented with a simple remote control interface on their device, which sends input to the game via PubNub.

### How to deploy to heroko

```bash
heroku login
git subtree push --prefix web heroku master
```
