"""
Task 3: Model-Based Reflex Agent Implementation

This module implements a model-based reflex agent that maintains internal state
and uses systematic exploration to ensure complete room coverage.
"""

import numpy as np
import random

# Global state for the model-based agent
agent_state = {
    'position': None,    # Will be inferred from bumpers
    'room_size': 5,      # Assumed room size
    'visited': set(),    # Set of visited coordinates
    'cleaned': set(),    # Set of cleaned coordinates
    'mode': 'LOCATE',    # Current mode: LOCATE, EXPLORE
    'exploration_path': [],  # Planned path for exploration
    'path_index': 0,     # Current position in exploration path
    'last_action': None  # Track last action for position inference
}

def reset_agent_state():
    """Reset the agent state for a new run."""
    global agent_state
    agent_state = {
        'position': None,
        'room_size': 5,
        'visited': set(),
        'cleaned': set(),
        'mode': 'LOCATE',
        'exploration_path': [],
        'path_index': 0,
        'last_action': None
    }

def infer_position_from_bumpers(bumpers):
    """Infer current position based on bumper sensors."""
    # This is a simplified approach - in reality, we'd need more sophisticated tracking
    # For now, we'll use a simple heuristic based on wall proximity
    
    # Count walls to estimate position
    wall_count = sum(bumpers.values())
    
    if wall_count == 2:
        # Corner position
        if bumpers['north'] and bumpers['west']:
            return (0, 0)  # Northwest corner
        elif bumpers['north'] and bumpers['east']:
            return (4, 0)  # Northeast corner
        elif bumpers['south'] and bumpers['west']:
            return (0, 4)  # Southwest corner
        elif bumpers['south'] and bumpers['east']:
            return (4, 4)  # Southeast corner
    elif wall_count == 1:
        # Edge position
        if bumpers['north']:
            return (2, 0)  # Top edge
        elif bumpers['south']:
            return (2, 4)  # Bottom edge
        elif bumpers['west']:
            return (0, 2)  # Left edge
        elif bumpers['east']:
            return (4, 2)  # Right edge
    
    # Default to center if no walls detected
    return (2, 2)

def generate_exploration_path():
    """Generate a systematic path to visit all squares."""
    path = []
    
    # Simple row-by-row exploration pattern
    for y in range(5):
        if y % 2 == 0:  # Even rows: left to right
            for x in range(5):
                path.append((x, y))
        else:  # Odd rows: right to left
            for x in range(4, -1, -1):
                path.append((x, y))
    
    return path

def get_available_directions(bumpers):
    """Get list of available directions (not blocked by walls)."""
    directions = []
    if not bumpers['north']:
        directions.append('north')
    if not bumpers['south']:
        directions.append('south')
    if not bumpers['east']:
        directions.append('east')
    if not bumpers['west']:
        directions.append('west')
    return directions

def model_based_reflex_agent(bumpers, dirty):
    """
    Model-based reflex agent that maintains state and navigates systematically.
    
    Args:
        bumpers: Dictionary with boolean values for north, south, east, west
        dirty: Boolean indicating if current square is dirty
    
    Returns:
        str: Action to take
    """
    global agent_state
    
    # Infer current position
    current_pos = infer_position_from_bumpers(bumpers)
    agent_state['position'] = current_pos
    agent_state['visited'].add(current_pos)
    
    # Rule 1: Always clean if dirty
    if dirty:
        agent_state['cleaned'].add(current_pos)
        agent_state['last_action'] = 'suck'
        return 'suck'
    
    # Mode: LOCATE - Try to reach a corner to establish position
    if agent_state['mode'] == 'LOCATE':
        # Check if we're at a corner
        wall_count = sum(bumpers.values())
        if wall_count >= 2:  # At a corner or edge
            agent_state['mode'] = 'EXPLORE'
            agent_state['exploration_path'] = generate_exploration_path()
            agent_state['path_index'] = 0
        else:
            # Move towards a corner (prefer northwest)
            if not bumpers['north']:
                agent_state['last_action'] = 'north'
                return 'north'
            elif not bumpers['west']:
                agent_state['last_action'] = 'west'
                return 'west'
            else:
                # Choose any available direction
                available = get_available_directions(bumpers)
                if available:
                    action = random.choice(available)
                    agent_state['last_action'] = action
                    return action
    
    # Mode: EXPLORE - Systematically visit squares
    if agent_state['mode'] == 'EXPLORE':
        # Check if we've visited all squares
        if len(agent_state['visited']) >= 25:  # 5x5 = 25 squares
            agent_state['last_action'] = 'suck'
            return 'suck'
        
        # Find next unvisited square
        next_target = None
        for i in range(agent_state['path_index'], len(agent_state['exploration_path'])):
            target = agent_state['exploration_path'][i]
            if target not in agent_state['visited']:
                next_target = target
                agent_state['path_index'] = i
                break
        
        if next_target:
            # Move towards target
            target_x, target_y = next_target
            current_x, current_y = current_pos
            
            # Calculate direction to target
            dx = target_x - current_x
            dy = target_y - current_y
            
            # Choose direction based on largest difference
            if abs(dx) > abs(dy):
                if dx > 0 and not bumpers['east']:
                    agent_state['last_action'] = 'east'
                    return 'east'
                elif dx < 0 and not bumpers['west']:
                    agent_state['last_action'] = 'west'
                    return 'west'
            else:
                if dy > 0 and not bumpers['south']:
                    agent_state['last_action'] = 'south'
                    return 'south'
                elif dy < 0 and not bumpers['north']:
                    agent_state['last_action'] = 'north'
                    return 'north'
        
        # If can't move towards target, choose any available direction
        available = get_available_directions(bumpers)
        if available:
            action = random.choice(available)
            agent_state['last_action'] = action
            return action
    
    # Fallback
    agent_state['last_action'] = 'suck'
    return 'suck'

if __name__ == "__main__":
    print("Model-Based Reflex Agent module loaded successfully!")
    print("Use model_based_reflex_agent() function for systematic exploration.")
    print("Don't forget to call reset_agent_state() before each simulation!")
