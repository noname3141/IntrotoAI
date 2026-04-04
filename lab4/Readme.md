#  Sudoku Solver (Python + PycoSAT)

This project provides a Python script `sudoku_solver.py` that solves Sudoku puzzles using the **SAT solver** approach powered by the `pycosat` library.

---

##  Project Structure

- `sudoku_solver.py` → Main solver script  
- `input.txt` → Input file containing the Sudoku puzzle  
- `output.txt` → Output file with the solved Sudoku (generated after execution)  

---

##  Requirements

- Python 3.x  
- `pycosat` library  

---

##  Setup & Execution

### 1. Create a Virtual Environment
```bash
python -m venv venv
````

### 2. Activate the Virtual Environment

#### On Linux / macOS:

```bash
source venv/bin/activate
```

#### On Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install pycosat
```

---

### 4. Run the Solver

Pass the input file as an argument:

```bash
python3 sudoku_solver.py input.txt
```

---

##  Input Format

* The input file (`input.txt`) contains a set of 81 char strings each being a **Single Game**.
* The digits `1–9` are used for filled cells.
* The `.` symbol is denoted for empty cells.

### Example `input.txt`:

```
53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79
```

---

##  Output

* The solved Sudoku is written to `output.txt`.
* Each solution of the game will appear on a new line.

### Example `output.txt`:

```
534678912672195348198342567859761423426853791713924856961537284287419635345286179
```

---

##  Notes

* Ensure the input format matches the expected structure.
* `output.txt` will be **created or overwritten** each time you run the script.
* Always activate the virtual environment before running the solver.

To deactivate the virtual environment:

```bash
deactivate
```

---

## Full Example Workflow

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install pycosat
python sudoku_solver.py input.txt
```

---

##  How It Works (Brief)

* The Sudoku puzzle is converted into a **Boolean SAT problem**.
* Constraints (rows, columns, boxes) are encoded as clauses.
* `pycosat` solves the SAT problem and returns a valid solution.

