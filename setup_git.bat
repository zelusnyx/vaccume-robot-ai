@echo off
echo Setting up Git repository for Vacuum Robot AI Assignment...
echo.

REM Initialize Git repository
echo [1/8] Initializing Git repository...
git init

REM Create .gitignore
echo [2/8] Creating .gitignore file...
echo # Jupyter Notebook checkpoints > .gitignore
echo .ipynb_checkpoints/ >> .gitignore
echo __pycache__/ >> .gitignore
echo *.pyc >> .gitignore
echo .vscode/ >> .gitignore
echo *.log >> .gitignore

REM Create README.md
echo [3/8] Creating README.md...
echo # Vacuum Cleaner Robot AI Assignment > README.md
echo. >> README.md
echo ## Overview >> README.md
echo Implementation of reflex-based agents for vacuum cleaner robot simulation. >> README.md
echo. >> README.md
echo ## Tasks Completed >> README.md
echo - Task 1: Environment simulation with PEAS compliance >> README.md
echo - Task 2: Simple reflex agent implementation >> README.md
echo - Task 3: Model-based reflex agent with state tracking >> README.md
echo - Task 4: Performance comparison study across room sizes >> README.md
echo - Task 5: Robustness analysis for various scenarios >> README.md
echo - Advanced: Imperfect sensor handling for graduate students >> README.md
echo. >> README.md
echo ## Usage >> README.md
echo Run all cells in Copy_of_robot_vacuum.ipynb to execute the complete analysis. >> README.md
echo. >> README.md
echo ## Requirements >> README.md
echo - Python 3.x >> README.md
echo - Jupyter Notebook >> README.md
echo - NumPy >> README.md
echo - Matplotlib >> README.md
echo - Pandas >> README.md

REM Add initial files
echo [4/8] Adding initial files...
git add .gitignore README.md
git commit -m "Initial commit: Add project structure and documentation"

REM Add Task 1
echo [5/8] Committing Task 1 - Environment implementation...
git add Copy_of_robot_vacuum.ipynb
git commit -m "Task 1: Implement vacuum environment simulation

- Create vacuum_environment() function with PEAS compliance
- Implement 5x5 room with random dirt placement (20%% probability)
- Add bumper and dirt sensors simulation
- Include agent position tracking and movement logic
- Add performance measurement (energy units used)
- Include verbose debugging output and room visualization"

REM Add Task 2
echo [6/8] Committing Task 2 - Simple reflex agent...
git add Copy_of_robot_vacuum.ipynb
git commit -m "Task 2: Implement simple reflex agent

- Create simple_reflex_agent() that reacts to sensor inputs
- Always clean when dirt is detected (suck action)
- Move randomly but avoid walls using bumper sensors
- Use clean, readable code with conversational comments
- Include comprehensive testing and demonstration"

REM Add Task 3
echo [7/8] Committing Task 3 - Model-based agent...
git add Copy_of_robot_vacuum.ipynb
git commit -m "Task 3: Implement model-based reflex agent

- Create model_based_reflex_agent() with internal state tracking
- Implement position inference from bumper sensors
- Add systematic exploration with row-by-row pattern
- Include state management for visited and cleaned squares
- Add mode switching (LOCATE -> EXPLORE)
- Comprehensive testing and performance comparison"

REM Add remaining tasks
echo [8/8] Committing remaining tasks...
git add Copy_of_robot_vacuum.ipynb
git commit -m "Tasks 4-5 + Advanced: Complete assignment

Task 4: Simulation study and performance analysis
- Run comprehensive comparison across room sizes (5x5, 10x10, 100x100)
- Execute 100 random runs for each configuration
- Generate performance tables and visualization graphs
- Analyze energy consumption, success rates, and efficiency metrics

Task 5: Robustness analysis for various scenarios
- Analyze agent performance under challenging conditions
- Rectangular rooms, irregular shapes, obstacles
- Imperfect sensors (10%% error rate)
- Provide detailed recommendations for each scenario

Advanced Task: Imperfect dirt sensor implementation
- Create imperfect_dirt_environment() with sensor error handling
- Implement improved_model_based_agent() with confidence tracking
- Add probabilistic cleaning strategies and sensor validation
- Graduate-level implementation for handling uncertainty"

echo.
echo ✅ Git repository setup complete!
echo.
echo Next steps:
echo 1. Create a new repository on GitHub.com
echo 2. Copy the repository URL
echo 3. Run the following commands:
echo    git remote add origin YOUR_GITHUB_URL_HERE
echo    git push -u origin main
echo.
echo Example:
echo    git remote add origin https://github.com/yourusername/vacuum-robot-ai.git
echo    git push -u origin main
echo.
pause
