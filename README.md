# Solar Data Discovery – Week 0 Challenge 

## This repository contains the Week 0 setup for the Solar Data Discovery challenge, including environment setup, folder structure, CI workflow and initial project documentation.

## Project Structure

 ├── .vscode/
 │   └── settings.json
 ├── .github/
 │   └── workflows/
 │       └── ci.yml
 ├── .gitignore
 ├── requirements.txt
 ├── README.md
 ├── src/
 ├── notebooks/
 │   ├── __init__.py
 │   └── README.md
 ├── tests/
 │   └── __init__.py
 └── scripts/
     ├── __init__.py
     └── README.md

## Setup Instructions
1. Clone the repository:
 ```bash
   git clone https://github.com/Mihret-Akalu/solar-challenge-week0.git
   cd solar-challenge-week0

2. how to all text markdown in vscode
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: .\venv\Scripts\activate

3. Install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt

4. Usage / How to Run the Project
```bash
## Usage
- Launch VS Code and select the interpreter from `venv/`.
- Open `notebooks/benin_eda.ipynb` to start analysis for Benin.
- Run `scripts/cleanup.py` to preprocess raw data etc.

5. Testing / CI
```bash
## Testing & CI
- We use GitHub Actions Workflow (`.github/workflows/ci.yml`) to install dependencies and run tests on each push or pull request.
- To run tests locally:
```bash
  pytest

6. Technologies / Dependencies
```bash
## Technologies
- Python 3.10
- pandas, numpy, matplotlib, seaborn
- GitHub Actions for CI


