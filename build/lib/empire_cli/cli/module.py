import typer, click, base64
from pathlib import Path
from ..api.rest import ServerConnection
from .utils import print_util
from . import cli_base

import tabulate

app = cli_base.EmpireTyper()

@click.pass_context
def fetch_module_list(ctx):
    # TODO: This does currently return a fully detailed list of modules with far more details than needed.
    # A more tailored API endpoint may serve us well and save some bandwidth here. 
    srv: ServerConnection = ctx.obj.empire_api
    return [module.name for module in srv.get_modules()]

@click.pass_context
def fetch_module_details(ctx, module_name):
    srv: ServerConnection = ctx.obj.empire_api
    return srv.get_module_details(module_name)


@app.callback(no_args_is_help=True)
def _common():
    """
    List and run modules. 
    """

@app.command("ls")
@app.command("list")
def list_modules():
    """
    Enumerate available modules. 
    """
    modules = fetch_module_list()
    output = print_util.shell_enumerate(modules)
    typer.echo(output)

@app.remote_component(fetch_module_list, fetch_module_details, name="run")
def execute_module(ctx: typer.Context, name: str, options):
    """
    Execute a module.  
    """
    srv: ServerConnection = ctx.obj.empire_api
    task_id = srv.execute_module(name, options)
    
    result = srv.get_task_result(name, task_id)
    print(result)
    while result['results'] is None:
        time.sleep(0.5)
        result = srv.get_task_result(name, task_id)
    
    print(result)