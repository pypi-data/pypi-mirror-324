# Wordle Solver

This project provides a Wordle solver that can be used as a command-line interface (CLI) tool or imported as a module in your Python code. SOWPODS is used as lexicon.

## Installation

### PyPI

```
pip install
```

### Manually
Clone the repository and navigate to the project directory:

```sh
git clone https://github.com/fmakdemir/wordle-solver.git
cd wordle-solver
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
poetry run wordlesolver --count 6
```

You can select the size of the word with 

### Importing and Using the Solver

You can also import the solver into your Python code:

```python
from wordlesolver import WordleSolver

solver = WordleSolver()
solution = solver.solve('your_word')
print(solution)
```

### Running Tests

To run the tests, use the following command:

```sh
pytest tests/
```

This will execute all the test cases in the `tests` directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
