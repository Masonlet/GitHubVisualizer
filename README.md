# GitHubVisualizer

GitHubVisualizer is a Python utility for exploring and visualizing activity in GitHub repositories. 

## Features

- **Repository Overview**: List all repositories for a user with commit previews
- **Contribution Graph**: GitHub-style heatmap showing commit activity over time
- **Smart Caching**: Automatic caching with 2-hour expiration to minimize API calls
- **Token Support**: Optional GitHub personal access token for higher rate limits

## Usage

Run the program and follow the prompts:
```bash
python main.py
```

You'll be prompted for:
- **GitHub username**: The user whose repositories you want to visualize
- **Refresh cache**: Whether to bypass cached data (y/n)
- **Access token**: Optional GitHub personal access token for higher rate limits

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager) 

## Building the Project

### 1. Clone the Repository
```bash
git clone https://github.com/Masonlet/GitHubVisualizer.git
cd GitHubVisualizer
```

### 2. Install required dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the main program
```bash
python main.py
```
