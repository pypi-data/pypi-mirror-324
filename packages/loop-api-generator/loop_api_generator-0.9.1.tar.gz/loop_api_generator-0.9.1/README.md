# team_project_api_generator

API Generator is a Python-based tool that allows users to define API structures and automatically generate API code. It is designed for developers and software engineers looking to quickly prototype RESTful APIs without writing boilerplate code.

# Overview

TODO: Overview of the project

# Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Contributing](#contributing)
4. [License](#license)
5. [Acknowledgements](#acknowledgements)

# Installation

## Prerequisites

- **Python** (preferably version 3.8+) https://www.python.org/
- **Git** https://git-scm.com/
- **Docker** https://www.docker.com/
- **Visual Studio Code (VSCode)** (or any other code editor) https://code.visualstudio.com/

## Step 1: Install VS Code Extensions

- **Black**: https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter
- **Flake8**: https://marketplace.visualstudio.com/items?itemName=ms-python.flake8
- **isort**: https://marketplace.visualstudio.com/items?itemName=ms-python.isort

## Step 2: Clone the Repository

1. Clone the repository:

   ```bash
   git clone https://github.com/annacwiklinska/team_project_api_generator

   or

   git clone git@github.com:annacwiklinska/team_project_api_generator.git
   ```

2. Change the directory to the project root:
   ```bash
    cd team_project_api_generator
   ```

## Step 3: Create and Activate a Virtual Environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

## Step 4: Install Dependencies

1. Install the dependencies by running:

   ```bash
   pip install -r requirements.txt -r requirements-dev.txt
   ```

## Step 5: Configure Git Hooks

1. Install the Git hooks defined in `.pre-commit-config.yaml`:

   ```bash
   pre-commit install
   ```

2. Manually run the hooks (optional):
   ```bash
   pre-commit run
   ```

## Step 6 (optional): Run Github actions locally

1. Install **act** https://nektosact.com/installation/index.html
2. Run **act** in the root directory of the project
   ```bash
   act
   ```
3. To run a specific workflow, use the `-j` flag:

   ```bash
   act -j <workflow-name>
   ```

   for example:

   ```bash
   act -j test
   ```

# Usage

### Run the Application

1. Run the application:

   ```bash
   cd src
   python3 -m api_generator.main 
   ```

### Running Tests

1. Run the tests:

   ```bash
   pytest -vs --color=yes tests
   ```

# Contributing

1. Clone the repository:

   ```bash
   git clone https://github.com/annacwiklinska/team_project_api_generator

   or

   git clone git@github.com:annacwiklinska/team_project_api_generator.git
   ```

2. Create an issue on GitHub https://github.com/annacwiklinska/team_project_api_generator/issues

3. Make your changes in a new branch:

   ```bash
   branch-name={issue-number}-{short-description}

   git checkout -b {branch-name}
   ```

4. Commit your changes:
   ```bash
   git add <files>
   git commit -m "Commit message"
   ```
5. Push the changes to your branch:
   ```bash
   git push --set-upstream origin {branch-name}
   ```
6. Create a pull request to merge your changes into the main branch.

# License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

# Acknowledgements

TODO: Acknowledgements
