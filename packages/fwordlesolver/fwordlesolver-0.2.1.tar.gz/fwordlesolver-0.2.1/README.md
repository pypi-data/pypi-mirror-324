# Wordle Solver

This project provides a Wordle solver that can be used as a command-line interface (CLI) tool or imported as a module in your Python code. SOWPODS is used as lexicon.

Suggests new words that are most likely to reduce the total results. Can filter current list of words with

## Installation

### PyPI

```
pip install fwordlesolver
```

### Manually
Clone the repository and navigate to the project directory:

```sh
git clone https://github.com/fmakdemir/fwordlesolver.git
cd fwordlesolver
```

Install Poetry if you haven't already. You can find the installation guide [here](https://python-poetry.org/docs/#installation).

Install the required dependencies using Poetry:

```sh
poetry install
```

## Usage

### Running as CLI

You can run the Wordle solver from the command line. Use the following command:

```sh
poetry run f-wordle-solver --word-size 6
```

You can select the size of the word with

### Importing and Using the Solver

You can also import the solver into your Python code:

```python
from fwordlesolver.solver import WordleSolver

solver = WordleSolver(6)
print(solver.get_suggestions())

solver.filter_word('blinks', '.x..x.')
print(solver.get_suggestions())
```

### Running Tests

This package uses [pytest](https://docs.pytest.org/) for running tests.

To run the tests, use the following command:

```sh
pytest
```

This will execute all the test cases in the `tests` directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
