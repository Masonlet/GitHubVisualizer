# GitHub Visualizer
![Tests](https://github.com/masonlet/github-visualizer/actions/workflows/test.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue.svg)]()   

GitHub Visualizer is a Python utility for exploring and visualizing activity in GitHub repositories. 

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Interactive Mode](#interactive-mode)
  - [Command-Line Mode](#command-line-mode)
  - [Command-Line Options](#command-line-options)
- [Running tests](#running-tests)
- [License](#license)

<br/> 



## Features
- **Repository Overview**: List all repositories for a user with commit previews
- **Contribution Graph**: GitHub-style heatmap showing commit activity over time
- **Smart Caching**: Automatic caching with 2-hour expiration to minimize API calls
- **Token Support**: Optional GitHub personal access token for higher rate limits

<br/>



## Prerequisites
- Python 3.6 or higher
- pip (Python package manager) 

## Installation

### From GitHub
```bash
pip install git+https://github.com/masonlet/github-visualizer.git
```

<br/>



## Usage

### Interactive Mode
Run the program without arguments and follow the prompts:
```bash
github-visualizer
```

You'll be prompted for:
- **GitHub username**: The user whose repositories you want to visualize
- **Refresh cache**: Whether to bypass cached data (y/n)
- **Access token**: Optional GitHub personal access token for higher rate limits

### Command-Line Mode
```bash
# Basic usage
github-visualizer masonlet

# With personal access token
github-visualizer masonlet --token ghp_xxxxx

# Refresh cached data
github-visualizer masonlet --refresh

# Show only last 26 weeks
github-visualizer masonlet --weeks 26

# Skip the contribution graph
github-visualizer masonlet --no-graph

# Skip the repository list
github-visualizer masonlet --no-list

# Combined options
github-visualizer masonlet --token ghp_xxxxx --refresh --weeks 26
```

### Command-Line Options
- `username` - GitHub username to visualize (optional in interactive mode)
- `--token`, `-t` - GitHub personal access token for higher rate limits
- `--refresh`, `-r` - Refresh cached data
- `--weeks`, `-w` - Number of weeks to display in graph (default: 52)
- `--no-graph` - Skip contribution graph display
- `--no-list` - Skip repository list display

<br/>



## Running Tests
### 1. Clone github-visualizer
```bash
git clone https://github.com/masonlet/github-visualizer.git
cd github-visualizer
```

### 2. Install in Development Mode
```bash
pip install -e .
```

### 3. Run Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_commit_api.py

# Run tests with flags
pytest -V
```

<br/>



## License
MIT License — see [LICENSE](./LICENSE) for details.
