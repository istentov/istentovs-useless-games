# useless-games repository doesn't forbid the modification of code (except if you don't know what you are doing)
# lib imports
import time
import fun
import inspect
import sys
import random
# volume imports
import volume1

print("""
    Ownership of Trương Nguyễn Huân, class 7A3 of 2024
    Enter "help" to receive a list of available commands
""")
time.sleep(1)

#####################################################################
# the hall of all command functions
def help():
    print("\n-------------------------------------------")
    for i in actions.keys():
        print(f"\"{i[0]}\": {i[1]}")
    print("-------------------------------------------\n")
    processCmds()

def ply():
    processCmds()
    fun.fun()

def volumeOne(episode):
    intepisode = int(episode)
    if intepisode > 5 or episode.isdigit() == False:
        print("Episode either doesn't exist or is alpha.")
        processCmds()
        return False
    for i in range(random.randint(3, 6)):
        sys.stdout.write(f'\rEpisode {episode} loading   | | | | |')
        time.sleep(0.1)
        sys.stdout.write(f'\rEpisode {episode} loading   / / / / /')
        time.sleep(0.1)
        sys.stdout.write(f'\rEpisode {episode} loading   - - - - -')
        time.sleep(0.1)
        sys.stdout.write(f'\rEpisode {episode} loading   \\ \\ \\ \\ \\')
        time.sleep(0.1)
    print("\n")
    getattr(volume1, "episode" + episode)()
    processCmds()

#####################################################################

actions = {
    ("help", "Returns commands from \"actions\" dict."): help,
    ("quit", "Terminates the program."): exit,
    ("fun", "\"Funnily\" opens a pygame window."): ply,
    ("vol1", "Volume 1 has 5 games and has parameter \"episode\"."): volumeOne,
}

# the central system of processing inputs and calls command from actions
# rules:
# the program doesn't run on a loop, if you want your function to be able to return to the terminal,
# please add "processCmds()" at the end of the function.

def processCmds():
    command = input("> ")
    for key in actions.keys():
        if key[0] in command:
            if len(inspect.getfullargspec(actions[key]).args) == 0 or command == "quit":
                actions[key]()
            else:
                splitCommand = command.split()
                actions[key](splitCommand[1])
            return True
    print(f"Invalid Command \"{command}\"")
    processCmds()

processCmds()
