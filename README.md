# marks-inquiry-2019
Mark's Inquiry project for Lesher Middle School, spring 2019

## The project

Mark wanted to learn about coding and game design for his "inquiry" (career exploration) project.

I decided to give him a pretty realistic experience:
- he worked in a team with me
- he owned some parts, but not the whole thing
- he did some work on his own, but also lots of pair programming
- he used git and github, including feature branches and pull requests

I suggested we work around the "snake" game, and he introduced me to slither.io (an online
multiplayer snake game). In the end, he created a simple version of the classic snake game,
using components that I created for a full multiplayer version similar to slither.io

This was his first real programming experience, so I ended up doing the bulk of the programming,
but I think the overall experience was very enlightening to him, and we had fun together.

## The final product

We used python 3 and the pygame engine as the basis.

*pygame aside:* I ended up creating a simple engine to make a bit of a paved path
for doing the common things (main loop running at a target FPS, event processing, timers,
a simple "scene" with layered objects). I had never worked with pygame before,
and it is much lower-level than I had expected -- really not very noob-friendly,
because it gives very little direction or help in creating a structured program.
I think a bit of a higher-level engine like this on top of pygame would really
make things more accessible for those who want to learn game coding...

Anyway, he programmed the basic single-player mode, using the snake that I built
for the multiplayer version. There's lots to be done for it to be a full classic
snake game, but that was not the focus.

The main focus was the multiplayer mode that he wanted to show off as part of
his project presentation. It's basically a simplified version of slither.io that
people can play using their own phones as the controller, connecting to the game
running on his computer.

## Setup

Install some dependencies:

First install python3 -- we tested this on both windows and linux:

```bash
py -m pip install -U pygame --user
py -m pip install -U pubnub --user
py -m pip install -U colormath --user
py -m pip install -U mamba expects doublex doublex-expects --user
```

He used the python installer for windows, which installs the interpeter as 'py' for some reason. For linux, just replace `py` with `python3`

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

We came up with this concept: people would walk up to his demo table and scan a QR code on their phones,
which opens up a simple html5-based joystick / controller they can use to play the game with others. It
is set up to allow up to 5 people to play at once, and any others that join wait in a queue until someone dies.

The multiplayer mode uses [PubNub](https://pubnub.com/) to provide a "second-screen" controller experience:
* Run the game in multiplayer mode, which will connect the game to PubNub to receive remote player input
* Visit https://marks-inquiry-2019.herokuapp.com/qr.html to load the multiplayer launcher.
* The launcher will display a QR code that players can scan on their phones to automatically join the game
* When players scan the QR code, they will be presented with a simple remote control interface on their device, which sends input to the game via PubNub.
* The background of the screen changes color to indicate the snake they are controlling.

### How to deploy to heroku

Only the `web` subtree is deployed to heroku, rather than the full repo:

```bash
heroku login
git subtree push --prefix web heroku master
```

### PubNub and Pygame

PubNub and pygame don't actually work very well together -- at least not very performant. PubNub runs
multiple threads, and that it makes it hard to keep a high or smooth frame rate while receiving
lots of messages.

I ended up using the python `multiprocessing` module to make all the PubNub stuff run in a separate
process. The `multiprocessing.Pipe` / `multiprocessing.Connection` made it really simple to transport
messages between the process, so that part ended up working really nicely.

After re-architecting with `multiprocessing`, the game is able to easily maintain ~60 FPS even with
5 players simultaneously connected. PubNub is really a pretty cool service.

