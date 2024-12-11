# ILBAI-LightUpSolver
Repository storing the code, write-up, and ReadME for our final project in Professor Selmer's Fall 2024 Intro to Logic Based AI Class 

## Purpose
- This project serves to solve Professor Selmer's final project topic, John LBAI-Engineer

## Baseline rules for the game
### General Rules/Info:
  Rules to the lightup/akari game can be found here: 
    https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/lightup.html#lightup
  
  - As a summary, all white areas/cells must be lit up (lights extend from the light in all 4 directions until it hits a black cell)
  - Each black box with a number must have that many lights directly adjacent to it (4 cardinal directions).
  - Lights must not be lit by another light (Lights should not have line of sight to each other)
  - Lights can only be placed on white cells

  All test grids setup before hand are available to be tested here (using the seed and game id links provided in the txt files):
    https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html 

### An overview of some important variable values:
  
  The grid is a 2D numpy array where:
      
      -1 = white cell (empty)
      -2 = black cell (no number)
      0-4 = black cell with number indicating adjacent lights

  The printed output of the grid has symbols representing the following:
      
      □ = white cell (empty)
      ■ = black cell (no number)
      0-4 = black cell with number indicating adjacent lights
      ★ = light 
      · = light beam (representing the beams that come from the lights)
      
  In the Light array we have values representing the following:
    
      0 = no light at [i][j]
      1 = there is a light at [i][j]

## How to setup

#### WARNING: DO NOT install "z3" as this is a deprecated AWS package

- This program was tested and run on miniconda 3 and python version 3.11.4 
- It utilizes dowloaded modules of z3, numpy, os, and time
  - All required modules are either included with python or can be dowloaded by running the [installation.py](installation.py) file we have included

Or if you are familiar with "pip" installing modules please run:
```pip install z3-solver numpy```

If you wish to uninstall these packages later, please run ```pip uninstall z3-solver numpy``` or just run [uninstall.py](uninstall.py)

## How to run
1. To run this program, run main.py
2. You should see a prompt in the terminal asking which file number you would like to run
3. Select a prompt and you will see the solver run through the steps to generate a solution to the game
4. You can verify the correctness of the solution through the online link provided at the end of the program

## Creating your own test cases
In order to create yout own test cases, you can create a txt file in the [grids](grids/) folder, from which the program will dynamically read it in and let you run as a test.

The txt file follows the following format:   
- For the array of {} fill in using the numbers from the [key for the grid array](#an-overview-of-some-important-variable-values)  provided above 
- Feel free to add more rows or columns, just ensure that it is rectangular 
- For the seed link, right click on link to puzzle by seed and copy
- For the game id link, right click on link to puzzle by game ID and copy
- Links for the seeds and game id can be found [here](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html)

#### Disclaimer: It is recommended that you generate a custom-grid with your specifications on the website provided above, copy it using the format below and then press solve to verify with our programs output.

      seed: {insert seed link}
      game_id: {insert game id link}

      {},{},{},{},{},{},{}
      {},{},{},{},{},{},{}
      {},{},{},{},{},{},{}
      {},{},{},{},{},{},{}
      {},{},{},{},{},{},{}
      {},{},{},{},{},{},{}
      {},{},{},{},{},{},{}

A filled out example file below:

      seed: https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html#7x7b20s4d2%23951739128355234
      game_id: https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html#7x7:cBg2c01aBb1e1bBa01cBg0c

      -1,-1,-1,-2,-1,-1,-1
      -1,-1,-1,-1,2,-1,-1
      -1,0,1,-1,-2,-1,-1
      1,-1,-1,-1,-1,-1,1
      -1,-1,-2,-1,-1,-1,-1
      -1,-1,-2,-1,-1,-1,-1
      -1,-1,-1,0,-1,-1,-1

