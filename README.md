# 2DayHackBot
This is a bot made using the RLBot framework that plays [rocket league](https://store.steampowered.com/app/252950/Rocket_League/). 
This bot was made in 2 days for the [RLBot July Hackathon](http://www.rlbot.org/), while working a normal 40 hour work week.
It doesn't work that well.

## About
This bot uses a combination of velocity and position PID control to make the car follow Cubic Hermite splines.
It can do this with reasonably good accuracy.

![A spline with pretty good accuracy](img/spline1.png?raw=true)
![A spline with kinda ok accuracy](img/spline2.png?raw=true)

Here green is the intended path, red is the path the bot drove along.

Unfortunately only an hour was dedicated to making the core ai of the bot after this system was finished, so it struggles
to hit the ball with its oversimplified state machine.

It will eventually score a goal given enough time.

## Changing the bot

- Bot behavior is controlled by `python_example/2daybot.py`
- Bot appearance is controlled by `python_example/appearance.cfg`

## Running the bot

See https://github.com/RLBot/RLBotPythonExample/wiki for RLBot documentation and tutorials.
