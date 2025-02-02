import typer

from fwordlesolver.solver import Solver

app = typer.Typer()


@app.command()
def solve(word_size: int = 4):
    solver = Solver(word_size)
    suffix = "\n " + "-" * word_size + "\n"
    while suggestions := solver.get_suggestions():
        print("Suggested: ", suggestions[:5])

        if len(suggestions) < 2:
            print("Reached end: ", suggestions)
            return suggestions[0] if suggestions else None

        word = typer.prompt("Enter a word:", prompt_suffix=suffix)
        places = typer.prompt("", prompt_suffix="")

        solver.filter_word(word, places)


if __name__ == "__main__":
    app()


def run():
    app()
