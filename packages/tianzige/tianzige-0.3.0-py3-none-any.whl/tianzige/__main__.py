"""Command line interface for Tianzige."""

import argparse
import sys
from . import __version__, create_tianzige

def main():
    """Entry point for the command line interface."""
    parser = argparse.ArgumentParser(
        description='Generate Tianzige (田字格) writing grid PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tianzige output.pdf                     Generate grid with default settings (A4, min 10 boxes)
  tianzige -p a5 output.pdf              Generate grid in A5 size
  tianzige -c "#000000" output.pdf       Generate grid with black lines
  tianzige -s 25 output.pdf              Generate grid with 25mm squares (no minimum)
  tianzige --min-horizontal 12 output.pdf Generate grid with at least 12 horizontal boxes
  tianzige --min-vertical 15 output.pdf  Generate grid with at least 15 vertical boxes
  tianzige --no-inner-grid output.pdf    Generate grid without inner lines
        """
    )
    
    parser.add_argument('output',
                      help='Output PDF file name')
    parser.add_argument('--version', '-v', action='version',
                      version=f'%(prog)s {__version__}')
    parser.add_argument('--color', '-c', default='#808080',
                      help='Line color in hex format (e.g., #808080)')
    parser.add_argument('--size', '-s', type=float,
                      help='Size of each square in mm (default: auto-calculated to fit minimum boxes)')
    parser.add_argument('--min-horizontal', type=int, default=None,
                      help='Minimum number of horizontal boxes (default: 10 if size not specified)')
    parser.add_argument('--min-vertical', type=int, default=None,
                      help='Minimum number of vertical boxes (default: 10 if size not specified)')
    parser.add_argument('--page-size', '-p', 
                      choices=['a4', 'a5', 'a6', 'a3', 'b4', 'b5', 'letter', 'legal'],
                      default='a4', 
                      help='Page size (default: a4)')
    parser.add_argument('--margin-top', type=float, default=15,
                      help='Top margin in mm')
    parser.add_argument('--margin-bottom', type=float, default=15,
                      help='Bottom margin in mm')
    parser.add_argument('--margin-left', type=float, default=20,
                      help='Left margin in mm')
    parser.add_argument('--margin-right', type=float, default=10,
                      help='Right margin in mm')
    parser.add_argument('--no-inner-grid', action='store_true',
                      help='Disable inner grid lines')
    
    args = parser.parse_args()
    
    try:
        create_tianzige(
            args.output,
            args.color,
            args.size,
            args.margin_top,
            args.margin_bottom,
            args.margin_left,
            args.margin_right,
            not args.no_inner_grid,
            args.page_size,
            args.min_horizontal,
            args.min_vertical
        )
        print(f"Generated Tianzige grid: {args.output}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
