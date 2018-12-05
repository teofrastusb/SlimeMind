# Slime Mind

![slime](images/slime_default_1.png "Slime Mind")

# Introduction
We made this game structure to allow us to write and test AI programs. Writers can use the example code to explore making their own AI. As a writer's code  advances they should submit it to be tested against other AI. Eventually tournaments will be run between all submissions. 

The current game is still being balanced and many of the parameters will likely be changed. Changes will be made in an attempt to balance the system but not destroy certain strategies. If someone figures out a way to win no matter what through complex AI or an out of the box strategy then good for them.

Eventually additional game mechanics may be added, and a new game with the same basic structure but additional mechanics may be released.
  
# Setup
## Suggested IDE
You are free to use whatever editor you want to create your AI. If you don't know where to start, we recommend [visual studio code](https://code.visualstudio.com/)

## Installing python
You must install Python 3.6 or later. See this [guide](https://docs.python-guide.org/starting/installation/) for steps.

## Installing libraries
You must install [arcade](http://arcade.academy/installation.html) to visualize the game.

# Running Matches
## Runners
There are multiple ways to run AIs against each other. All of them are available in `main.py`. For instructions try
```
python main.py --help
```
## Configuration
There are some configuration options in `config.ini`, such as the ability to turn off visualization. 
Note: the multi-match runner does not visualize matches, regardless of the `render` configuration.

# Game Mechanics
## Setup
Slime Mind is played on a map that is broken into squares with a set number of columns and rows. The exact number of columns and rows may be changed in the config.py file. However the standard number that will be used for tournaments and such is:
30 columns and 15 rows (likely this will be tweaked). At the start of a game plants, rocks, and slimes are put randomly on the map and mirrored across x and y so player's have an even playing field.

## Turns
Player AIs control each individual slime from their team every turn. Once a game begins each object will be given a single round per turn.
* Rocks go first and do nothing.
* Plants will go next and run on a defined AI described in the Game Pieces section of this document.
* Slimes will then go alternating between each team until all slimes have gone.
Then the map will update and the turn will be completed.

## Game Pieces
There are three types of game piece in this game. All of them are given the following attributes:
```
x - This is the column index of the game piece (starting from 0)
y - This is the row index of the game piece (starting from 0)
```

### Rocks
Rocks are only meant to get in the way. They are placed at the beginning of the game and cannot be moved or destroyed.

### Plants
Plants are the food source for the slimes. All plants have the following attributes:
```
max_level - This is the highest level a plant can reach.
level - Used to calculate the maximum health of the plant. 
max_hp - This is the most health a plant can have.
current_hp - This is the current health of a plant.
```
Plants are placed at the beginning of the game at level 1 with a set amount of health. Every round the plant has a % chance to level up, which increases maximum health regains some lost health. Once a plant reaches its maximum level it will gain the ability to spread seeds. Every round a max level plant has a % chance to spread a seed to one of the 8 squares surrounding it. If a plant succeeds in seeding another plant at level 1 will be placed in the target square. Plants at maximum level will change color in the visualizer. 

### Slimes
Slimes are the gamepieces controlled by the submitted AI code and will be used to determine which AI wins a game. Each slime has the following attributes:
```
xp - Used to calculate the level of a slime.
max_level - This is the highest level a slime can reach.
level - Used to calculate the attack and maximum health of the slime. 
maximum_hp - This is the most health a slime can have.
current_hp - This is the current health of a slime.
attack -  This is the amount of health a slime or plant will lose when this slime bites it.
```
Slimes are placed at the beginning of the game at level 1. A slimes attack and maximum HP increase as they level up. The table below shows the minimum XP for a slime to become each level and the other attributes for that level. The full equation can be found in the code.
```
xp	level	attack	max_hp
1	1	3	11
2	2	4	13
6	3	7	18
15	4	10	23
33	5	13	31
62	6	16	40
106	7	20	50
169	8	24	61
254	9	29	75
368	10	33	89
513	11	38	105
695	12	43	122


```
Every turn each slime is given a round to take a single action determined by the submitted AI. Invalid commands and AI that exceed a set timeout are ignored, skipping that slime's round. Valid commands are applied immediately, before the next slime's round begins. Note that the game state given the AI is immutable, so changes are not reflected in the game engine.

# Commands
There are only 10 acceptable commands that a slime can accept. They are:
```
LEFT
RIGHT
UP
DOWN
BITELEFT
BITERIGHT
BITEUP
BITEDOWN
SPLIT
MERGE
```

### Move Commands
The four move commands available to slimes are:
```
LEFT
RIGHT
UP
DOWN
```
Move commands attempt to move the slime in the corresponding direction (`LEFT` moves the slime to the square that has the same y value but an x value of one less etc...). If the target square is occupied by another game piece or is past the edge of the map the move will be ignored.

### Bite Commands
The four bite commands available to slimes are:
```
BITELEFT
BITERIGHT
BITEUP
BITEDOWN
```
Bite commands attempt to attack nearby gamepieces in a particular direction. If there is not a valid target in the location then the slime will do nothing for its round. If there is a slime or plant object in the target location then that slime or plant will have its `current_health` reduced by the biting slimes `attack`. The biting slime will also have its `current_hp` increased by 1 and its `xp` increased by 1.

### Split Command
The only split command available to slimes is:
```
SPLIT
```
To split a slime must be at least level 4. Splitting creates a new level 1 slime in any empty adjacent square. This divides the `xp` of the splitting slime by 4 (rounding down).

### Merge Commands
The only merge command available to slimes is:
```
MERGE
```
This sets a slime as ready to merge. If an adjacent friendly slime is ready to merge it will be destroyed and the initiating slime will gain its `xp`. Every turn all slimes are set to no longer ready to merge, so you must coordinate merging within a single turn.

# Victory conditions
The game will continue until turn 1000 or until one team has 0 slimes. Scores for each team are calculated based on the remaining slimes. This score calculation is based solely on the slimes level _not_ on its total xp. The table below shows a simplified level to score ratio. The full equation can be found in the code.
```
level	points
1	0.2
2	0.4
3	1.6
4	5.2
5	13.7
6	29.9
7	57.7
8	101.7
9	167.0
10	259.7
11	386.7
12	555.3

```
The team with the most total points at the end of the game wins.

# Writing a Custom AI
Your AI must inherit the `PlayerBase` class and override the `command_slime` method. See the `playerCode` folder for examples.

# Packaging

Run the following commands to package this library:
```
rm -rf dist build */*.egg-info *.egg-info
python3 setup.py sdist bdist_wheel
twine upload dist/*
```