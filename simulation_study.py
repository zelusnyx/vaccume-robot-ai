"""
Task 4: Simulation Study and Performance Analysis

This module runs comprehensive performance comparisons across different room sizes
and generates tables and graphs for analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from environment import vacuum_environment
from simple_agent import simple_randomized_agent, simple_reflex_agent
from model_based_agent import model_based_reflex_agent, reset_agent_state

def run_simulation_study():
    """Run comprehensive simulation study across different room sizes."""
    
    # Define room sizes and number of runs
    room_sizes = [5, 10, 100]
    num_runs = 100
    
    # Initialize results storage
    results = {
        'room_size': [],
        'agent_type': [],
        'energy': [],
        'success': [],
        'run_number': []
    }
    
    print("Starting Simulation Study...")
    print("=" * 60)
    
    for room_size in room_sizes:
        print(f"\nTesting room size: {room_size}x{room_size}")
        print("-" * 40)
        
        # Test each agent type
        agents = [
            ('Randomized', simple_randomized_agent),
            ('Simple Reflex', simple_reflex_agent),
            ('Model-Based Reflex', model_based_reflex_agent)
        ]
        
        for agent_name, agent_func in agents:
            print(f"  Testing {agent_name} agent...")
            
            energies = []
            successes = []
            
            for run in range(num_runs):
                # Reset model-based agent state for each run
                if agent_name == 'Model-Based Reflex':
                    reset_agent_state()
                
                # Run simulation with higher max_steps for larger rooms
                max_steps = room_size * room_size * 10  # Allow more steps for larger rooms
                
                energy, success, steps = vacuum_environment(
                    agent_func, 
                    room_size=room_size, 
                    max_steps=max_steps,
                    verbose=False
                )
                
                energies.append(energy)
                successes.append(success)
                
                # Store results
                results['room_size'].append(room_size)
                results['agent_type'].append(agent_name)
                results['energy'].append(energy)
                results['success'].append(success)
                results['run_number'].append(run + 1)
            
            # Print summary for this agent
            avg_energy = np.mean(energies)
            success_rate = np.mean(successes) * 100
            std_energy = np.std(energies)
            
            print(f"    Average energy: {avg_energy:.1f} ± {std_energy:.1f}")
            print(f"    Success rate: {success_rate:.1f}%")
            print(f"    Min energy: {min(energies)}")
            print(f"    Max energy: {max(energies)}")
    
    return pd.DataFrame(results)

def create_performance_visualization(results_df):
    """Create visualization graphs for performance comparison."""
    
    # Set up the plotting style
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Agent Performance Comparison Across Room Sizes', fontsize=16, fontweight='bold')

    # 1. Average Energy Consumption by Room Size
    ax1 = axes[0, 0]
    for agent_type in ['Randomized', 'Simple Reflex', 'Model-Based Reflex']:
        agent_data = results_df[results_df['agent_type'] == agent_type]
        energy_by_size = agent_data.groupby('room_size')['energy'].mean()
        ax1.plot(energy_by_size.index, energy_by_size.values, marker='o', linewidth=2, label=agent_type)

    ax1.set_xlabel('Room Size')
    ax1.set_ylabel('Average Energy Consumption')
    ax1.set_title('Average Energy Consumption by Room Size')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')

    # 2. Success Rate by Room Size
    ax2 = axes[0, 1]
    for agent_type in ['Randomized', 'Simple Reflex', 'Model-Based Reflex']:
        agent_data = results_df[results_df['agent_type'] == agent_type]
        success_by_size = agent_data.groupby('room_size')['success'].mean() * 100
        ax2.plot(success_by_size.index, success_by_size.values, marker='s', linewidth=2, label=agent_type)

    ax2.set_xlabel('Room Size')
    ax2.set_ylabel('Success Rate (%)')
    ax2.set_title('Success Rate by Room Size')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    ax2.set_ylim(0, 105)

    # 3. Energy Distribution Box Plot (5x5 room)
    ax3 = axes[1, 0]
    room_5_data = results_df[results_df['room_size'] == 5]
    agent_types = ['Randomized', 'Simple Reflex', 'Model-Based Reflex']
    energy_data = [room_5_data[room_5_data['agent_type'] == agent]['energy'].values for agent in agent_types]

    box_plot = ax3.boxplot(energy_data, labels=agent_types, patch_artist=True)
    colors = ['lightcoral', 'lightblue', 'lightgreen']
    for patch, color in zip(box_plot['boxes'], colors):
        patch.set_facecolor(color)

    ax3.set_ylabel('Energy Consumption')
    ax3.set_title('Energy Distribution (5x5 Room)')
    ax3.grid(True, alpha=0.3)

    # 4. Performance Efficiency (Energy per Square Cleaned)
    ax4 = axes[1, 1]
    for agent_type in ['Randomized', 'Simple Reflex', 'Model-Based Reflex']:
        agent_data = results_df[results_df['agent_type'] == agent_type]
        efficiency_data = []
        
        for room_size in [5, 10, 100]:
            size_data = agent_data[agent_data['room_size'] == room_size]
            # Calculate efficiency as energy per square (assuming all squares need cleaning)
            total_squares = room_size * room_size
            avg_energy = size_data['energy'].mean()
            efficiency = avg_energy / total_squares
            efficiency_data.append(efficiency)
        
        ax4.plot([5, 10, 100], efficiency_data, marker='^', linewidth=2, label=agent_type)

    ax4.set_xlabel('Room Size')
    ax4.set_ylabel('Energy per Square')
    ax4.set_title('Energy Efficiency (Energy per Square)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_xscale('log')

    plt.tight_layout()
    plt.show()

def print_performance_table(results_df):
    """Print performance comparison table."""
    
    print("Performance Comparison Table")
    print("=" * 60)

    # Calculate summary statistics
    summary_stats = results_df.groupby(['room_size', 'agent_type']).agg({
        'energy': ['mean', 'std', 'min', 'max'],
        'success': 'mean'
    }).round(1)

    # Create a clean table for display
    performance_table = []

    for room_size in [5, 10, 100]:
        row = [f"{room_size}x{room_size}"]
        
        for agent_type in ['Randomized', 'Simple Reflex', 'Model-Based Reflex']:
            try:
                stats = summary_stats.loc[(room_size, agent_type)]
                avg_energy = stats[('energy', 'mean')]
                success_rate = stats[('success', 'mean')] * 100
                row.append(f"{avg_energy:.1f} ({success_rate:.1f}%)")
            except KeyError:
                row.append("N/A")
        
        performance_table.append(row)

    # Display table
    print(f"{'Size':<10} {'Randomized Agent':<20} {'Simple Reflex Agent':<25} {'Model-based Reflex Agent':<30}")
    print("-" * 90)

    for row in performance_table:
        print(f"{row[0]:<10} {row[1]:<20} {row[2]:<25} {row[3]:<30}")

    print("\nNote: Values shown as 'Average Energy (Success Rate %)'")
    print("=" * 60)

if __name__ == "__main__":
    print("Running simulation study...")
    results = run_simulation_study()
    print_performance_table(results)
    create_performance_visualization(results)
    print("Simulation study complete!")
