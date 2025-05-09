# Step-by-Step CFG to CNF Conversion

This modified version of the CFG2CNF converter shows the detailed step-by-step process of converting a Context-Free Grammar (CFG) to Chomsky Normal Form (CNF), following the procedure outlined in COMP2270.

## Conversion Procedure

The conversion to Chomsky Normal Form follows these sequential steps:

### 1. Remove all ε-rules (removeEps)
This step eliminates all productions of the form A → ε (epsilon):
- First, identify all nullable non-terminals (those that can directly derive ε)
- Find additional nullable non-terminals (those that derive only nullable symbols)
- For each production containing nullable non-terminals, add versions with them removed
- Remove all epsilon productions

### 2. Remove all unit productions 
This step eliminates all productions of the form A → B where B is a non-terminal:
- Identify all unit productions (where the right side is a single non-terminal)
- Replace each unit production A → B with A → α for each production B → α
- Repeat until no unit productions remain

### 3. Remove mixed productions
This step handles productions with both terminals and non-terminals:
- Create a new non-terminal for each terminal symbol (e.g., a → A')
- Replace all occurrences of terminals in mixed productions with their non-terminal equivalents

### 4. Break down long productions
This step handles productions with more than 2 non-terminals:
- For each production A → X₁X₂...Xₙ where n > 2
- Create new non-terminals for groups of symbols
- Replace the original production with a set of productions with at most 2 non-terminals on the right side

## Final Chomsky Normal Form

After these transformations, the grammar will be in Chomsky Normal Form where each production is either:
- A → a (a non-terminal produces a single terminal)
- A → BC (a non-terminal produces exactly two non-terminals)

## Implementation Details

The implementation shows each transformation step with detailed output:
- The original grammar is displayed
- Each transformation is applied sequentially
- Intermediate steps are shown in detail
- The final grammar in CNF is displayed

## Example Conversion

The program walks through examples like:

### Example: S → X | Y, X → xX | xZ, Y → yY | yZ, Z → abcM, M → NP, N → n | ε, P → p | ε

1. **Remove ε-rules**:
   - Identify N, P as nullable
   - Recognize that M is also nullable (derives only nullable symbols)
   - Generate new productions by removing nullable symbols

2. **Remove unit productions**:
   - Replace S → X with productions from X
   - Replace S → Y with productions from Y
   - Replace M → N and M → P with their productions

3. **Remove mixed productions**:
   - Create new non-terminals for each terminal (a, b, c, x, y, n, p)
   - Replace all mixed productions with pure non-terminal versions

4. **Break down long productions**:
   - Break productions with more than 2 non-terminals
   - Create new non-terminals for each group

## Usage

To run the program with step-by-step output:

```bash
python3 main.py
```

Then input your grammar rules in the format `A -> α | β` followed by `*` when complete.

For automated tests with various grammar examples:

```bash
./test.py
```
