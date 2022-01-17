# myoCollectOnWins

Gesture data collection on windows.

The keybinds to control the gesture collection app

#### Up: Connects myo armband to the PC

#### Right: Next gesture

#### Left: Last gesture

#### Space: Start the timer

#### Esc: Disconnects myo armband from the PC and save the data (sorted in folder)



## Installation (Anaconda)

Create an environment with packages installation (Use requirements.txt)

After installing the Anaconda, open the Anaconda Prompt and enter the following commands:

conda create -name "env_name" python = 3.8.8

conda activate "env_name"

conda install --file requirements.txt


## Usage

1) Run "python main_collect.py" and enter the subject ID (4-digits e.g. 0001)
2) Press "Up" to connect the myo to the laptop. Once it is connected, the EMG bars will be moving up and down.
3) Press "Space" to start the timer. There are 3 seconds for preprataion (Red) and 5 seconds for recording (Green)
4) Press "Right" if you want to change to another gesture 
5) In the end, press "Esc" to stop the application and save the data. 
