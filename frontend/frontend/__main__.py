import typer

app = typer.Typer()

@app.command()
def dummy():
    return True

if __name__ == "__main__":
    app()