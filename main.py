# Author: Max Base (Modified with step-by-step conversion)
# Date: 2020/06/17 (Updated 2025)
# Web: maxbase.org
# Repo: https://github.com/BaseMax/CFG2CNF
import sys
import copy

print("Enter your grammar with `S -> ab` similar style. You can split productions by | and write rules in different lines.")
print("When you're done, type * on a new line:")

# Dictionary to track new non-terminals created for terminals
terminal_mappings = {}

# Available non-terminal symbols
available_symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# Parse input grammar
rules = {}
while True:
    line = input()
    if line == "*":
        break
    parts = line.split("->")
    if len(parts) != 2:
        print(f"Error parsing line: {line}. Format should be 'A -> B'")
        continue
    
    non_terminal = parts[0].strip()
    productions = parts[1].strip().split("|")
    
    if non_terminal not in rules:
        rules[non_terminal] = []
    
    for production in productions:
        production = production.strip()
        if production not in rules[non_terminal]:
            rules[non_terminal].append(production)

# Helper function to find an available non-terminal symbol
def get_new_non_terminal(grammar):
    used_symbols = set(grammar.keys())
    for symbol in available_symbols:
        if symbol not in used_symbols:
            return symbol
    raise Exception("Error: Ran out of available non-terminal symbols!")

# Helper function to print the current grammar state
def print_grammar_state(grammar, title):
    print(f"\n{title}:")
    for non_terminal in sorted(grammar.keys()):
        productions = " | ".join(grammar[non_terminal]) if grammar[non_terminal] else "$"
        print(f"{non_terminal} -> {productions}")

# STEP 1: Remove all ε-rules
def remove_epsilon_rules(grammar):
    print("\n=== STEP 1: Removing ε-rules (removeEps) ===")
    print("This step eliminates all productions of the form A → ε")
    
    # Create a deep copy of the grammar to avoid modifying during iteration
    result = copy.deepcopy(grammar)
    
    # Step 1.1: Find all nullable non-terminals (those that can derive ε directly)
    nullable = set()
    
    print("Step 1.1: Identifying nullable non-terminals...")
    for nt, productions in result.items():
        if "$" in productions:
            nullable.add(nt)
            print(f"  - {nt} is nullable (derives ε directly)")
            
            # Remove epsilon production
            result[nt].remove("$")
    
    # Step 1.2: Find additional nullable non-terminals (those that derive only nullable symbols)
    changed = True
    while changed:
        changed = False
        for nt, productions in result.items():
            if nt not in nullable:
                for prod in productions:
                    if all(symbol in nullable for symbol in prod) and prod:
                        nullable.add(nt)
                        print(f"  - {nt} is nullable (derives only nullable symbols)")
                        changed = True
                        break
    
    print(f"Nullable non-terminals: {', '.join(sorted(nullable))}")
    
    # Step 1.3: For each production containing nullable non-terminals, add versions with them removed
    print("\nStep 1.3: Adding productions with nullable symbols removed...")
    for nt in list(result):
        new_productions = []
        for prod in result[nt]:
            # Skip empty productions
            if not prod:
                continue
                
            # Find all nullable symbols in this production
            nullable_positions = [i for i, symbol in enumerate(prod) if symbol in nullable]
            
            # Generate all combinations of removing nullable symbols (except removing all)
            if nullable_positions:
                print(f"  - Processing {nt} -> {prod} which contains nullable symbols")
                
                # Generate all subsets of nullable positions
                from itertools import combinations
                for r in range(1, len(nullable_positions) + 1):
                    for positions_to_remove in combinations(nullable_positions, r):
                        # Convert to list for easier manipulation
                        prod_list = list(prod)
                        # Remove symbols from right to left to maintain indices
                        for pos in sorted(positions_to_remove, reverse=True):
                            del prod_list[pos]
                        
                        # Only add if not empty and not already there
                        new_prod = ''.join(prod_list)
                        if new_prod and new_prod not in result[nt] and new_prod not in new_productions:
                            new_productions.append(new_prod)
                            print(f"    Added new production: {nt} -> {new_prod}")
        
        # Add all new productions
        result[nt].extend(new_productions)
    
    # Remove any empty productions
    for nt in list(result):
        result[nt] = [p for p in result[nt] if p]
    
    print_grammar_state(result, "Grammar after removing ε-rules")
    return result

# STEP 2: Remove all unit productions (A → B)
def remove_unit_productions(grammar):
    print("\n=== STEP 2: Removing unit productions ===")
    print("This step eliminates all productions of the form A → B where B is a non-terminal")
    
    # Create a deep copy of the grammar
    result = copy.deepcopy(grammar)
    
    # Keep track of all non-terminals
    non_terminals = set(result.keys())
    
    # Keep looping until no more unit productions can be removed
    changed = True
    while changed:
        changed = False
        
        for nt in list(result):
            # Find all unit productions
            unit_productions = [(i, prod) for i, prod in enumerate(result[nt]) 
                                if len(prod) == 1 and prod in non_terminals]
            
            if unit_productions:
                # Process unit productions
                for idx, unit in sorted(unit_productions, reverse=True):
                    print(f"  - Found unit production: {nt} -> {unit}")
                    
                    # Remove the unit production
                    result[nt].pop(idx)
                    
                    # Add all the productions of the referenced non-terminal
                    for replacement in result[unit]:
                        if replacement not in result[nt]:
                            result[nt].append(replacement)
                            print(f"    Replaced with: {nt} -> {replacement}")
                    
                    changed = True
    
    print_grammar_state(result, "Grammar after removing unit productions")
    return result

# STEP 3: Remove mixed productions (with terminals and non-terminals)
def remove_mixed_productions(grammar):
    print("\n=== STEP 3: Removing mixed productions ===")
    print("This step handles productions with both terminals and non-terminals")
    
    result = copy.deepcopy(grammar)
    
    # Dictionary to map terminals to their non-terminal replacements
    global terminal_mappings
    
    # First, create new non-terminals for each terminal
    for nt in list(result):
        for i, prod in enumerate(result[nt]):
            for j, symbol in enumerate(prod):
                if symbol.islower():  # Terminal
                    if symbol not in terminal_mappings:
                        new_nt = get_new_non_terminal(result)
                        terminal_mappings[symbol] = new_nt
                        result[new_nt] = [symbol]
                        print(f"  - Created new non-terminal {new_nt} -> {symbol}")
    
    # Replace terminals in mixed productions
    for nt in list(result):
        for i, prod in enumerate(list(result[nt])):
            # Check if this is a mixed production (has length > 1 and includes terminals)
            if len(prod) > 1 and any(c.islower() for c in prod):
                print(f"  - Processing mixed production: {nt} -> {prod}")
                
                # Create a new production with terminals replaced
                new_prod = ""
                for symbol in prod:
                    if symbol.islower():  # Terminal
                        new_prod += terminal_mappings[symbol]
                    else:
                        new_prod += symbol
                
                # Replace the old production
                result[nt][i] = new_prod
                print(f"    Replaced with: {nt} -> {new_prod}")
    
    print_grammar_state(result, "Grammar after removing mixed productions")
    return result

# STEP 4: Break down productions with more than 2 non-terminals
def break_long_productions(grammar):
    print("\n=== STEP 4: Breaking down long productions ===")
    print("This step handles productions with more than 2 non-terminals")
    
    result = copy.deepcopy(grammar)
    
    # Process each non-terminal's productions
    for nt in list(result):
        i = 0
        while i < len(result[nt]):
            prod = result[nt][i]
            
            # If the production has more than 2 symbols
            if len(prod) > 2:
                print(f"  - Breaking down long production: {nt} -> {prod}")
                
                # Create a new non-terminal for the tail
                new_nt = get_new_non_terminal(result)
                tail = prod[1:]
                
                # Add the new production
                result[new_nt] = [tail]
                
                # Replace the original production
                result[nt][i] = prod[0] + new_nt
                
                print(f"    Created: {new_nt} -> {tail}")
                print(f"    Replaced with: {nt} -> {prod[0]}{new_nt}")
            else:
                i += 1
    
    # We may need to repeat this process for the newly created rules
    changed = True
    while changed:
        changed = False
        
        for nt in list(result):
            i = 0
            while i < len(result[nt]):
                prod = result[nt][i]
                
                if len(prod) > 2:
                    # Create a new non-terminal for the last two symbols
                    new_nt = get_new_non_terminal(result)
                    last_two = prod[-2:]
                    
                    # Add the new production
                    result[new_nt] = [last_two]
                    
                    # Replace the original production
                    result[nt][i] = prod[:-2] + new_nt
                    
                    print(f"  - Further breaking: {nt} -> {prod}")
                    print(f"    Created: {new_nt} -> {last_two}")
                    print(f"    Replaced with: {nt} -> {prod[:-2]}{new_nt}")
                    
                    changed = True
                else:
                    i += 1
    
    print_grammar_state(result, "Grammar after breaking long productions")
    return result

# Main function to apply the CNF conversion
def convert_to_cnf(grammar):
    print("\n==================================================")
    print("CONVERTING GRAMMAR TO CHOMSKY NORMAL FORM")
    print("==================================================")
    
    print_grammar_state(grammar, "Original Grammar")
    
    # Apply each transformation step
    step1_grammar = remove_epsilon_rules(grammar)
    step2_grammar = remove_unit_productions(step1_grammar)
    step3_grammar = remove_mixed_productions(step2_grammar)
    step4_grammar = break_long_productions(step3_grammar)
    
    print("\n==================================================")
    print("CONVERSION COMPLETE")
    print("==================================================")
    
    print_grammar_state(step4_grammar, "Final Grammar in Chomsky Normal Form")
    return step4_grammar

# Process the input grammar
convert_to_cnf(rules)
