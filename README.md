This is the source code for a school project done by Bouke van der Bijl and Yannick Middelkoop

It is an implementation of pong which uses the webcam to control the paddles

## Requirements to run

* [PyBox2d](http://code.google.com/p/pybox2d/)
* [OpenCV (compiled with some GIL locks removed)](https://github.com/boukevanderbijl/opencv)
* [PyGame](http://www.pygame.org/news.html)
* Python 2.7
* 2 green circles like these:

![paddles](http://i.imgur.com/s6F8KJD.jpg)

## How to play the game

Execute `python game.py` to play the game. You'll be greeted by a menu that you can control with the arrow keys and enter to select an option. After selecting something the game starts immediately.

Just stand in front of your webcam and (with sufficient lighting) the game should detect the green circles and move the in-game paddles to their correct positions. Try to bounce the ball into your opponent's endzone!

