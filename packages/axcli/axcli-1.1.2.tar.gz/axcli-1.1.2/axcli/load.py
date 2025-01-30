import click, os
import axinite.tools as axtools

@click.command("load")
@click.argument("input_path", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument("output_path", type=click.Path(exists=False, file_okay=True, dir_okay=True), default="")
def load(input_path, output_path=""):
    "Load a system from a file."
    args = axtools.read(input_path)
    if output_path != "":
        if os.path.isdir(output_path): axtools.load(args, f"{output_path}/{args.name}.ax", verbose=True) 
        else: axtools.load(args, output_path, verbose=True)
    else: axtools.load(args, f"{args.name}.ax", verbose=True)