"""This module provides the what-llm-can-i-run CLI."""
from typing import Optional
import typer
from whatllm import __app_name__, __version__, VRAM_ERROR
from .ram import get_total_ram
from .vram import get_machine_spec
from .llm_list import get_llm_list, list_to_excel
import logging


app = typer.Typer()


def _version_callback(value: bool) -> None:

    if value:

        typer.echo(f"{__app_name__} v{__version__}")

        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


# gets hardware spec (or throws an error) and then exits
@app.command(name="spec")
def get_hardware_info():
    """
    """
    typer.echo(f"Total RAM: {get_total_ram()} GiB")

    try:
        spec = get_machine_spec()
        typer.echo(f'Platform: {spec[0]}')
        typer.echo(f'Device: {spec[1]}')
        typer.echo(f'Total VRAM: {spec[2]} GiB')
    except Exception as e:
        typer.echo(f"Error: {e}")
        logging.error(e)
    finally:
        typer.Exit()

# get a list of recommended LLMs to run based on hardware spec
@app.command(name="list")
def get_llm_list_wrapper(
    quantize: bool = typer.Option(False, "--quantize", "-q", help="Enable quantization."),
    precision: str = typer.Argument("bf16", help="Precision of the model.")
):
    """ Returns a list of potentially suitable LLMs to run locally.
    Parameters:
        quantize: bool to consider quantization.
        precision: str representing the precision of the model.
    Returns:
        None
    """
    # check the quantize flag
    if quantize:
        if precision.lower() not in ['int4', 'int8']: # wrong quantization precision
            typer.echo("Quantize only to: 'int4' or 'int8'.")
            raise typer.Exit()
        else: # some models cannot be quantized
            typer.echo("Theoretically, you may try to quantize the following models for best performance.")
    else: # no quantization
        if precision.lower() in ['fp32']:
            typer.echo("You may try upcasting the following models from their default fp16/bf16 precision.")
        if precision.lower() not in ['fp16', 'bf16', 'fp32']:
            typer.echo("Precision should be: 'fp16', 'bf16', or 'fp32'.")
            raise typer.Exit()

    # retrieves hardware specs first
    capacity = get_total_ram()  # default to CPU inference
    # check GPU availability
    if (vram := get_machine_spec()[2]):
        capacity = vram  # GPU inference most likely faster than CPU, even if VRAM < RAM

    llm_list = get_llm_list(precision, capacity)
    typer.echo(llm_list)


@app.command("fetch")
def fetch_new_leaderboard():
    """
    
    """
    try:
        list_to_excel()
        typer.echo("Successfully fetched from Open LLM Leaderboard.")
    except Exception as e:
        typer.echo(f"Error fetching from Open LLM Leaderboard: {e}")
        logging.error(e)