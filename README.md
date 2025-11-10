# GitHub Visualizer

GitHub Visualizer is a Python utility for exploring and visualizing activity in GitHub repositories. 

## Features

- **Repository Overview**: List all repositories for a user with commit previews
- **Contribution Graph**: GitHub-style heatmap showing commit activity over time
- **Smart Caching**: Automatic caching with 2-hour expiration to minimize API calls
- **Token Support**: Optional GitHub personal access token for higher rate limits

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager) 

## Usage

### Interactive Mode

Run the program without arguments and follow the prompts:
```bash
python main.py
```

You'll be prompted for:
- **GitHub username**: The user whose repositories you want to visualize
- **Refresh cache**: Whether to bypass cached data (y/n)
- **Access token**: Optional GitHub personal access token for higher rate limits

### Command-Line Mode

```bash
# Basic usage
python main.py Masonlet

# With personal access token
python main.py Masonlet --token ghp_xxxxx

# Refresh cached data
python main.py Masonlet --refresh

# Show only last 26 weeks
python main.py Masonlet --weeks 26

# Skip the contribution graph
python main.py Masonlet --no-graph

# Skip the repository list
python main.py Masonlet --no-list

# Combined
python main.py Masonlet --token ghp_xxxxx --refresh --weeks 26
```

## Building the Project

### 1. Clone the Repository
```bash
git clone https://github.com/masonlet/github-visualizer.git
cd github-visualizer
```

### 2. Install required dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the main program
```bash
python main.py
```
