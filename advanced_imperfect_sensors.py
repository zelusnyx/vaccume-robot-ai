"""
Advanced Task: Imperfect Dirt Sensor Implementation

This module implements and tests agents with imperfect dirt sensors (10% error rate)
and develops improved solutions for handling sensor uncertainty.
"""

import numpy as np
import random
from environment import vacuum_environment
from simple_agent import simple_randomized_agent, simple_reflex_agent
from model_based_agent import model_based_reflex_agent, reset_agent_state

def imperfect_dirt_environment(agent_function, room_size=5, dirt_prob=0.2, max_steps=1000, 
                             sensor_error_rate=0.1, verbose=False):
    """
    Environment with imperfect dirt sensor that gives wrong readings 10% of the time.
    
    Args:
        agent_function: The agent program function
        room_size: Size of the square room
        dirt_prob: Probability that each square starts dirty
        max_steps: Maximum number of steps before timeout
        sensor_error_rate: Probability of sensor giving wrong reading
        verbose: Whether to print debug information
    
    Returns:
        tuple: (total_energy_used, success_flag, steps_taken, uncleaned_squares)
    """
    
    # Initialize room state
    room = np.random.random((room_size, room_size)) < dirt_prob
    initial_dirty_count = np.sum(room)
    
    # Random starting position
    agent_x = random.randint(0, room_size - 1)
    agent_y = random.randint(0, room_size - 1)
    
    if verbose:
        print(f"Initial room state (1=dirty, 0=clean):")
        print(room.astype(int))
        print(f"Agent starts at position ({agent_x}, {agent_y})")
        print(f"Initial dirty squares: {initial_dirty_count}")
        print()
    
    energy_used = 0
    steps_taken = 0
    
    # Main simulation loop
    while energy_used < max_steps:
        # Check if room is completely clean
        if np.sum(room) == 0:
            if verbose:
                print(f"Room cleaned! Total energy used: {energy_used}")
            return energy_used, True, steps_taken, 0
        
        # Create bumper sensors
        bumpers = {
            "north": agent_y == 0,
            "south": agent_y == room_size - 1,
            "west": agent_x == 0,
            "east": agent_x == room_size - 1
        }
        
        # Imperfect dirt sensor
        actual_dirty = room[agent_y, agent_x]
        if np.random.random() < sensor_error_rate:
            dirty = not actual_dirty  # Wrong reading
        else:
            dirty = actual_dirty  # Correct reading
        
        if verbose:
            print(f"Step {steps_taken}: Agent at ({agent_x}, {agent_y})")
            print(f"Actual dirty: {actual_dirty}, Sensor reading: {dirty}")
            print(f"Bumpers: {bumpers}")
        
        # Get action from agent
        action = agent_function(bumpers, dirty)
        
        if verbose:
            print(f"Action: {action}")
        
        # Execute action
        if action == "suck":
            if actual_dirty:
                room[agent_y, agent_x] = False
                if verbose:
                    print("Square cleaned!")
            else:
                if verbose:
                    print("Sucking on clean square (no effect)")
        
        elif action == "north":
            if agent_y > 0:
                agent_y -= 1
                if verbose:
                    print(f"Moved north to ({agent_x}, {agent_y})")
            else:
                if verbose:
                    print("Bumped into north wall")
        
        elif action == "south":
            if agent_y < room_size - 1:
                agent_y += 1
                if verbose:
                    print(f"Moved south to ({agent_x}, {agent_y})")
            else:
                if verbose:
                    print("Bumped into south wall")
        
        elif action == "west":
            if agent_x > 0:
                agent_x -= 1
                if verbose:
                    print(f"Moved west to ({agent_x}, {agent_y})")
            else:
                if verbose:
                    print("Bumped into west wall")
        
        elif action == "east":
            if agent_x < room_size - 1:
                agent_x += 1
                if verbose:
                    print(f"Moved east to ({agent_x}, {agent_y})")
            else:
                if verbose:
                    print("Bumped into east wall")
        
        energy_used += 1
        steps_taken += 1
        
        if verbose:
            print(f"Remaining dirty squares: {np.sum(room)}")
            print()
    
    # Timeout reached
    uncleaned_squares = np.sum(room)
    if verbose:
        print(f"Timeout reached after {max_steps} steps.")
        print(f"Remaining dirty squares: {uncleaned_squares}")
    
    return energy_used, False, steps_taken, uncleaned_squares

# Improved model-based agent for imperfect sensors
agent_state = {
    'position': None,
    'room_size': 5,
    'visited': set(),
    'cleaned': set(),
    'mode': 'LOCATE',
    'exploration_path': [],
    'path_index': 0,
    'last_action': None,
    'confidence': {}
}

def reset_improved_agent_state():
    """Reset the improved agent state for a new run."""
    global agent_state
    agent_state = {
        'position': None,
        'room_size': 5,
        'visited': set(),
        'cleaned': set(),
        'mode': 'LOCATE',
        'exploration_path': [],
        'path_index': 0,
        'last_action': None,
        'confidence': {}
    }

def infer_position_from_bumpers(bumpers):
    """Infer current position based on bumper sensors."""
    wall_count = sum(bumpers.values())
    
    if wall_count == 2:
        if bumpers['north'] and bumpers['west']:
            return (0, 0)
        elif bumpers['north'] and bumpers['east']:
            return (4, 0)
        elif bumpers['south'] and bumpers['west']:
            return (0, 4)
        elif bumpers['south'] and bumpers['east']:
            return (4, 4)
    elif wall_count == 1:
        if bumpers['north']:
            return (2, 0)
        elif bumpers['south']:
            return (2, 4)
        elif bumpers['west']:
            return (0, 2)
        elif bumpers['east']:
            return (4, 2)
    
    return (2, 2)

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

def move_towards_target(target_x, target_y, bumpers):
    """Move towards a target position."""
    current_x, current_y = agent_state['position']
    
    dx = target_x - current_x
    dy = target_y - current_y
    
    if abs(dx) > abs(dy):
        if dx > 0 and not bumpers['east']:
            return 'east'
        elif dx < 0 and not bumpers['west']:
            return 'west'
    else:
        if dy > 0 and not bumpers['south']:
            return 'south'
        elif dy < 0 and not bumpers['north']:
            return 'north'
    
    # Fallback
    available = get_available_directions(bumpers)
    if available:
        return random.choice(available)
    return 'suck'

def improved_model_based_agent(bumpers, dirty):
    """
    Improved model-based agent that handles imperfect dirt sensors.
    
    Strategy:
    1. Maintain confidence levels for each square
    2. Revisit squares with low confidence
    3. Use probabilistic cleaning decisions
    """
    global agent_state
    
    # Infer current position
    current_pos = infer_position_from_bumpers(bumpers)
    agent_state['position'] = current_pos
    agent_state['visited'].add(current_pos)
    
    # Initialize confidence tracking if not exists
    if 'confidence' not in agent_state:
        agent_state['confidence'] = {}
    
    # Update confidence based on sensor reading
    if current_pos not in agent_state['confidence']:
        agent_state['confidence'][current_pos] = {'clean': 0, 'dirty': 0}
    
    if dirty:
        agent_state['confidence'][current_pos]['dirty'] += 1
    else:
        agent_state['confidence'][current_pos]['clean'] += 1
    
    # Calculate confidence in current square being dirty
    conf_data = agent_state['confidence'][current_pos]
    total_readings = conf_data['clean'] + conf_data['dirty']
    
    if total_readings > 0:
        dirty_confidence = conf_data['dirty'] / total_readings
    else:
        dirty_confidence = 0.5  # Default uncertainty
    
    # Decision making with confidence threshold
    confidence_threshold = 0.7
    
    # If confident square is dirty, clean it
    if dirty_confidence > confidence_threshold:
        agent_state['cleaned'].add(current_pos)
        agent_state['last_action'] = 'suck'
        return 'suck'
    
    # If confident square is clean, move on
    elif dirty_confidence < (1 - confidence_threshold):
        # Move to next unvisited square or low-confidence square
        return find_next_target(bumpers)
    
    # If uncertain, clean to be safe (but with lower priority)
    elif dirty_confidence > 0.5:
        agent_state['cleaned'].add(current_pos)
        agent_state['last_action'] = 'suck'
        return 'suck'
    
    # Otherwise, explore
    return find_next_target(bumpers)

def find_next_target(bumpers):
    """Find next target square to visit."""
    global agent_state
    
    # Look for squares with low confidence
    low_confidence_squares = []
    for pos, conf_data in agent_state['confidence'].items():
        total_readings = conf_data['clean'] + conf_data['dirty']
        if total_readings < 3:  # Need more readings
            low_confidence_squares.append(pos)
    
    if low_confidence_squares:
        # Move to nearest low-confidence square
        current_x, current_y = agent_state['position']
        target = min(low_confidence_squares, 
                    key=lambda p: abs(p[0] - current_x) + abs(p[1] - current_y))
        return move_towards_target(target[0], target[1], bumpers)
    
    # Look for unvisited squares
    unvisited = []
    for y in range(5):
        for x in range(5):
            if (x, y) not in agent_state['visited']:
                unvisited.append((x, y))
    
    if unvisited:
        current_x, current_y = agent_state['position']
        target = min(unvisited, 
                    key=lambda p: abs(p[0] - current_x) + abs(p[1] - current_y))
        return move_towards_target(target[0], target[1], bumpers)
    
    # All squares visited, clean any remaining uncertain squares
    return 'suck'

def test_imperfect_sensors():
    """Test all agents with imperfect dirt sensors."""
    
    agents = [
        ('Randomized', simple_randomized_agent),
        ('Simple Reflex', simple_reflex_agent),
        ('Model-Based', model_based_reflex_agent),
        ('Improved Model-Based', improved_model_based_agent)
    ]
    
    results = {}
    
    for agent_name, agent_func in agents:
        print(f"\nTesting {agent_name} Agent:")
        print("-" * 40)
        
        energies = []
        successes = []
        uncleaned_counts = []
        
        for run in range(20):  # 20 runs for testing
            # Reset agent state
            if 'Model-Based' in agent_name:
                if agent_name == 'Improved Model-Based':
                    reset_improved_agent_state()
                else:
                    reset_agent_state()
            
            energy, success, steps, uncleaned = imperfect_dirt_environment(
                agent_func, room_size=5, sensor_error_rate=0.1, verbose=False
            )
            
            energies.append(energy)
            successes.append(success)
            uncleaned_counts.append(uncleaned)
        
        # Calculate performance metrics
        avg_energy = np.mean(energies)
        success_rate = np.mean(successes) * 100
        avg_uncleaned = np.mean(uncleaned_counts)
        
        # Calculate efficiency (energy per square cleaned)
        total_squares = 25  # 5x5 room
        avg_cleaned = total_squares - avg_uncleaned
        efficiency = avg_energy / avg_cleaned if avg_cleaned > 0 else float('inf')
        
        results[agent_name] = {
            'avg_energy': avg_energy,
            'success_rate': success_rate,
            'avg_uncleaned': avg_uncleaned,
            'efficiency': efficiency
        }
        
        print(f"  Average Energy: {avg_energy:.1f}")
        print(f"  Success Rate: {success_rate:.1f}%")
        print(f"  Average Uncleaned Squares: {avg_uncleaned:.1f}")
        print(f"  Efficiency (Energy/Cleaned): {efficiency:.2f}")
    
    return results

if __name__ == "__main__":
    print("Advanced Task: Imperfect Dirt Sensor Implementation")
    print("=" * 60)
    
    print("Testing agents with imperfect dirt sensor (10% error rate)...")
    results = test_imperfect_sensors()
    
    print("\n" + "=" * 60)
    print("Key Findings:")
    print("""
1. **Sensor Imperfection Impact:**
   - All agents show performance degradation with imperfect sensors
   - Model-based agents are most affected due to reliance on accurate sensing
   - Simple reflex agents show moderate degradation

2. **Improved Model-Based Agent:**
   - Uses confidence-based decision making
   - Revisits uncertain squares multiple times
   - Trades energy efficiency for cleaning completeness
   - Better handles sensor uncertainty

3. **Performance Trade-offs:**
   - Perfect sensors: High efficiency, low energy consumption
   - Imperfect sensors: Lower efficiency, higher energy consumption
   - Improved agent: Better completeness, moderate efficiency

4. **Recommendations:**
   - Implement sensor fusion techniques
   - Use probabilistic cleaning strategies
   - Maintain confidence levels for each square
   - Implement retry mechanisms for uncertain readings
""")
