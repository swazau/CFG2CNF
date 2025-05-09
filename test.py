#!/usr/bin/env python3
# Test script for CFG2CNF with step-by-step conversion demonstration

import subprocess
import sys

def test_grammar(grammar, description):
    print(f"\n===== Testing {description} =====")
    print("Input Grammar:")
    print("\n".join(grammar))
    print("\nRunning conversion...")
    
    # Run the main.py script with the grammar as input
    process = subprocess.run(
        ["python3", "main.py"],
        input="\n".join(grammar) + "\n*\n",
        text=True,
        capture_output=True
    )
    
    # Print the output
    print(process.stdout)
    
    if process.returncode != 0:
        print(f"Error (return code {process.returncode}):")
        print(process.stderr)
        return False
    
    return True

def main():
    # Test cases that demonstrate all the steps in the conversion process
    test_cases = [
        (
            ["S -> SaB | aB", "B -> bB | $"],
            "Grammar with epsilon production (Step 1)"
        ),
        (
            ["S -> X | Y", "X -> xX | xZ", "Y -> yY | yZ", "Z -> abcM", "M -> NP", "N -> n | $", "P -> p | $"],
            "Grammar from the assignment (All steps)"
        ),
        (
            ["S -> A | B | C", "A -> a", "B -> b", "C -> c"],
            "Grammar with unit productions (Step 2)"
        ),
        (
            ["S -> aBc", "B -> b"],
            "Grammar with mixed terminals and non-terminals (Step 3)"
        ),
        (
            ["S -> ABC", "A -> a", "B -> b", "C -> c"],
            "Grammar with long productions (Step 4)"
        )
    ]
    
    # Run the tests
    success = 0
    for grammar, description in test_cases:
        if test_grammar(grammar, description):
            success += 1
    
    print(f"\nTests: {success}/{len(test_cases)} successful")

if __name__ == "__main__":
    main()
