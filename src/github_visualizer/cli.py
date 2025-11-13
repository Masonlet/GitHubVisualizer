"""
Command-line argument parsing.

Handles CLI arguments for non-interactive usage.
"""

import argparse
from .config import DEFAULT_WEEKS

def parse_args():
  """
  Parse command-line arguments.

  Returns:
    Parsed arguments namespace
  """
  parser = argparse.ArgumentParser(
    description='GitHub Visualizer',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
  Examples:
    %(prog)s Masonlet
    %(prog)s Masonlet --token ghp_xxxxx
    %(prog)s Masonlet --refresh --weeks 26
    %(prog)s Masonlet --no-graph
    """
  )

  parser.add_argument(
    'username',
    nargs='?',
    help="GitHub username to visualize"
  )
  parser.add_argument(
    '--token', '-t',
    help='GitHub personal access token for higher rate limits'
  )
  parser.add_argument(
    '--refresh', '-r',
    action='store_true',
    help='Refresh cached data'
  )
  parser.add_argument(
    '--weeks', '-w',
    type=int,
    default=DEFAULT_WEEKS,
    help=f'Number of weeks to display in graph (default: {DEFAULT_WEEKS})'
  )
  parser.add_argument(
    '--no-graph',
    action='store_true',
    help='Skip contribution graph display'
  )
  parser.add_argument(
    '--no-list',
    action='store_true',
    help='Skip repository list display'
  )
  return parser.parse_args()