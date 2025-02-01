import marimo

__generated_with = "0.10.19"
app = marimo.App()


@app.cell
def _(Datasette):
    df = Datasette().get_polars(database="sqlite", table="chickweight")

    df.select("weight", "time", "diet")
    return (df,)


@app.cell
def _():
    import marimo as mo
    from datasette_marimo import Datasette
    return Datasette, mo


if __name__ == "__main__":
    app.run()
