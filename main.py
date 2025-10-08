"""
Main Runner for Vacuum Cleaner Robot AI Assignment

This module provides a unified interface to run all components of the assignment.
"""

import sys
import os

def run_environment_demo():
    """Run Task 1: Environment demonstration."""
    print("=" * 60)
    print("TASK 1: ENVIRONMENT DEMONSTRATION")
    print("=" * 60)
    
    from environment import vacuum_environment
    from simple_agent import simple_randomized_agent
    
    print("Testing environment with simple randomized agent...")
    energy, success, steps = vacuum_environment(simple_randomized_agent, room_size=5, verbose=True)
    print(f"\nResults: Success={success}, Energy={energy}, Steps={steps}")

def run_agent_comparison():
    """Run Task 2-3: Agent comparison."""
    print("\n" + "=" * 60)
    print("TASKS 2-3: AGENT COMPARISON")
    print("=" * 60)
    
    from environment import vacuum_environment
    from simple_agent import simple_randomized_agent, simple_reflex_agent
    from model_based_agent import model_based_reflex_agent, reset_agent_state
    
    agents = [
        ('Randomized', simple_randomized_agent),
        ('Simple Reflex', simple_reflex_agent),
        ('Model-Based', model_based_reflex_agent)
    ]
    
    print("Running 10 tests for each agent...")
    for agent_name, agent_func in agents:
        print(f"\n{agent_name} Agent:")
        energies = []
        successes = []
        
        for run in range(10):
            if agent_name == 'Model-Based':
                reset_agent_state()
            
            energy, success, steps = vacuum_environment(agent_func, room_size=5, verbose=False)
            energies.append(energy)
            successes.append(success)
        
        print(f"  Average Energy: {sum(energies)/len(energies):.1f}")
        print(f"  Success Rate: {sum(successes)/len(successes)*100:.1f}%")

def run_simulation_study():
    """Run Task 4: Simulation study."""
    print("\n" + "=" * 60)
    print("TASK 4: SIMULATION STUDY")
    print("=" * 60)
    
    try:
        from simulation_study import run_simulation_study, print_performance_table, create_performance_visualization
        
        print("Running comprehensive simulation study...")
        print("Note: This may take a few minutes for 100x100 room...")
        
        results = run_simulation_study()
        print_performance_table(results)
        create_performance_visualization(results)
        
    except ImportError as e:
        print(f"Error importing simulation study: {e}")
        print("Make sure all required packages are installed: numpy, matplotlib, pandas")

def run_robustness_analysis():
    """Run Task 5: Robustness analysis."""
    print("\n" + "=" * 60)
    print("TASK 5: ROBUSTNESS ANALYSIS")
    print("=" * 60)
    
    from robustness_analysis import analyze_robustness, print_detailed_analysis
    
    analyze_robustness()
    print_detailed_analysis()

def run_advanced_task():
    """Run Advanced Task: Imperfect sensors."""
    print("\n" + "=" * 60)
    print("ADVANCED TASK: IMPERFECT SENSORS")
    print("=" * 60)
    
    try:
        from advanced_imperfect_sensors import test_imperfect_sensors
        
        results = test_imperfect_sensors()
        
    except ImportError as e:
        print(f"Error importing advanced task: {e}")

def main():
    """Main function to run the complete assignment."""
    
    print("VACUUM CLEANER ROBOT AI ASSIGNMENT")
    print("=" * 60)
    print("This program will run all tasks of the assignment.")
    print("Choose what to run:")
    print("1. Environment Demo (Task 1)")
    print("2. Agent Comparison (Tasks 2-3)")
    print("3. Simulation Study (Task 4)")
    print("4. Robustness Analysis (Task 5)")
    print("5. Advanced Task (Imperfect Sensors)")
    print("6. Run Everything")
    print("0. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == '0':
                print("Goodbye!")
                break
            elif choice == '1':
                run_environment_demo()
            elif choice == '2':
                run_agent_comparison()
            elif choice == '3':
                run_simulation_study()
            elif choice == '4':
                run_robustness_analysis()
            elif choice == '5':
                run_advanced_task()
            elif choice == '6':
                print("Running complete assignment...")
                run_environment_demo()
                run_agent_comparison()
                run_simulation_study()
                run_robustness_analysis()
                run_advanced_task()
                print("\n" + "=" * 60)
                print("ASSIGNMENT COMPLETE!")
                print("=" * 60)
                break
            else:
                print("Invalid choice. Please enter 0-6.")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()
