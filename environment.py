"""
Task 1: Vacuum Environment Implementation

This module implements the PEAS-compliant simulation environment for the vacuum cleaner robot.
It includes room initialization, agent positioning, sensor simulation, and action execution.
"""

import numpy as np
import random

def vacuum_environment(agent_function, room_size=5, dirt_prob=0.2, max_steps=1000, verbose=False):
    """
    Simulation environment for vacuum cleaner robot.
    
    Args:
        agent_function: The agent program function
        room_size: Size of the square room (default 5x5)
        dirt_prob: Probability that each square starts dirty (default 0.2)
        max_steps: Maximum number of steps before timeout (default 1000)
        verbose: Whether to print debug information
    
    Returns:
        tuple: (total_energy_used, success_flag, steps_taken)
    """
    
    # 1. Build the room: each square has a dirt_prob probability of being dirty
    room = np.random.random((room_size, room_size)) < dirt_prob
    
    # 2. Put the robot in a random spot
    x = random.randint(0, room_size - 1)
    y = random.randint(0, room_size - 1)

    energy_used = 0
    steps_taken = 0

    if verbose:
        print("Starting room (1=dirty, 0=clean):")
        print(room.astype(int))
        print(f"Robot starts at ({x}, {y})\n")

    # 3. Keep going until energy runs out
    while energy_used < max_steps:
        # Stop if everything is clean
        if np.sum(room) == 0:
            if verbose:
                print(f"All clean in {energy_used} steps!")
            return energy_used, True, steps_taken
        
        # 4. Robot sensors
        bumpers = {
            "north": y == 0,
            "south": y == room_size - 1,
            "west": x == 0,
            "east": x == room_size - 1
        }
        dirty_here = room[y, x]

        if verbose:
            print(f"Step {energy_used}: at ({x},{y}), dirty={dirty_here}")

        # 5. Ask the robot what to do
        action = agent_function(bumpers, dirty_here)

        # 6. Carry out the action
        if action == "suck":
            room[y, x] = False   # clean the square
            if verbose: print(" → Sucked up dirt")
        elif action == "north" and not bumpers["north"]:
            y -= 1
            if verbose: print(" → Moved north")
        elif action == "south" and not bumpers["south"]:
            y += 1
            if verbose: print(" → Moved south")
        elif action == "west" and not bumpers["west"]:
            x -= 1
            if verbose: print(" → Moved west")
        elif action == "east" and not bumpers["east"]:
            x += 1
            if verbose: print(" → Moved east")
        else:
            if verbose: print(f" → Invalid or bump action: {action}")

        energy_used += 1
        steps_taken += 1

    # If we ran out of steps
    if verbose:
        print(f"Stopped after {max_steps} steps. Dirt left: {np.sum(room)}")
    return energy_used, False, steps_taken

def display_room_state(room, agent_x, agent_y):
    """
    Display the current room state with agent position.
    """
    room_size = room.shape[0]
    print("Room state (D=dirty, C=clean, A=agent):")
    for y in range(room_size):
        row = ""
        for x in range(room_size):
            if x == agent_x and y == agent_y:
                row += "A "
            elif room[y, x]:
                row += "D "
            else:
                row += "C "
        print(row)
    print()

if __name__ == "__main__":
    print("Environment module loaded successfully!")
    print("Use vacuum_environment() function to run simulations.")
