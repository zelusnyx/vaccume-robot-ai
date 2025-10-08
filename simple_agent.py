"""
Task 2: Simple Reflex Agent Implementation

This module implements a simple reflex agent that reacts to sensor inputs.
The agent cleans dirt when detected and moves randomly while avoiding walls.
"""

import random

def simple_reflex_agent(bumpers, dirty):
    """
    Simple reflex agent that reacts to bumper and dirt sensors.
    
    Args:
        bumpers: Dictionary with boolean values for north, south, east, west
        dirty: Boolean indicating if current square is dirty
    
    Returns:
        str: Action to take ("north", "south", "east", "west", "suck")
    """
    # If the robot sees dirt, it always cleans first
    if dirty:
        return "suck"
    
    # Otherwise, check which directions are safe (no wall)
    available_directions = []
    if not bumpers["north"]:
        available_directions.append("north")
    if not bumpers["south"]:
        available_directions.append("south")
    if not bumpers["east"]:
        available_directions.append("east")
    if not bumpers["west"]:
        available_directions.append("west")
    
    # If no safe moves (shouldn't really happen), just suck
    if not available_directions:
        return "suck"
    
    # Pick one safe direction randomly
    return random.choice(available_directions)

def simple_randomized_agent(bumpers, dirty):
    """
    Simple randomized agent that ignores sensors (for comparison).
    
    Args:
        bumpers: Dictionary with boolean values for north, south, east, west
        dirty: Boolean indicating if current square is dirty
    
    Returns:
        str: Random action
    """
    import numpy as np
    actions = ["north", "east", "west", "south", "suck"]
    return np.random.choice(actions)

if __name__ == "__main__":
    print("Simple Reflex Agent module loaded successfully!")
    print("Available agents:")
    print("- simple_reflex_agent: Cleans dirt and avoids walls")
    print("- simple_randomized_agent: Random actions (for comparison)")
