"""
Example usage of the breakpoint analysis pipeline.

This script demonstrates how to analyze moment-angle data from a participant.
Modify the file path and column indices to analyze your own data.
"""

from utils.pipeline import breakpoint

def main():
    breakpoint('data/example_data.txt', angle_column=1, moment_column=2, standing_column=5)

if __name__ == "__main__":
    main()







