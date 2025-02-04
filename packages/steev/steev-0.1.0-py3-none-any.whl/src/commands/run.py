from pathlib import Path

import click

from src.core import Runner, client
from src.core.websocket_client import WebSocketClient
from src.utils.cache import set_cache
from src.utils.credentials import cred
from src.utils.parser import parse_input
from src.utils.print import typing_print, typing_prompt, print_line


def validate_kwargs(ctx, param, value):
    if not value:
        return {}

    result = {}
    for arg in value:
        # Handle comma-separated format: "epoch=1,lr=3"
        if "," in arg:
            pairs = arg.split(",")
        # Handle space-separated format: "epoch=1 lr=3"
        else:
            pairs = arg.split()

        for pair in pairs:
            if "=" not in pair:
                raise click.BadParameter(f"'{pair}' must be in format 'key=value'")
            k, v = pair.split("=", 1)
            result[k.strip()] = v.strip()

    return result


class ExtensionType(click.Path):
    def __init__(self, ext):
        self.ext = ext
        super().__init__(exists=True)

    def convert(self, value, param, ctx):
        if not value.endswith(self.ext):  # type: ignore
            raise click.BadParameter(f"File must have a {self.ext} extension")
        value = Path(value)
        return super().convert(value, param, ctx)


@click.command(name="run")
@click.argument("train_file", type=ExtensionType(".py"))
@click.option("--cfg", type=ExtensionType(".yaml"), help="Path to the configuration file")
@click.option(
    "--steev-cfg",
    type=ExtensionType(".cfg"),
    help="Path to the steev config file",
    default="steev.cfg",
)
@click.option(
    "--kwargs",
    type=str,
    help=("Additional arguments in format: key=value,key2=value2" " or 'key=value key2=value2'" "(wrapped in quotes)"),
    multiple=True,
    callback=validate_kwargs,
)
def run(train_file: Path, cfg: str, kwargs: dict, steev_cfg: str):
    """Run the training code

    Train file must be a python file which contains the training code.

    Arguments:

        TRAIN_FILE: Path to the training file

    example:

        \b
        steev run train.py
        steev run train.py --cfg train.yaml
        steev run train.py --kwargs epoch=10,lr=0.001,batch_size=32...
        steev run train.py --kwargs "epoch=10 lr=0.001 batch_size=32..."
    """

    if kwargs and cfg:
        click.echo(
            click.style("[Error] Config path and kwargs cannot be used together", fg="red"),
            err=True,
        )
        return

    if not cred.verify():
        click.echo(
            click.style("[Error] You are not logged in, Please log in first", fg="red"),
            err=True,
        )
        return

    typing_print("\nSteev here! 👋 Let me take a look at your code...", color="blue", keywords=["Steev"])

    yaml_args = parse_input(cfg)
    steev_arguments = parse_input(steev_cfg)

    arguments = {**yaml_args, **kwargs}

    typing_print(f"You added the following arguments: {arguments}", color="green", keywords=[str(arguments)])
    typing_print(f"and I got your training code: {train_file}", color="green", keywords=[str(train_file)])

    with open(train_file, "r") as f:
        train_code = f.read()

    response = client.send_code(train_code, arguments, steev_arguments)
    experiment_id = response["experiment_id"]

    typing_print(f"Here is your experiment ID: {experiment_id}", color="green", keywords=[str(experiment_id)])
    typing_print("Please keep it safe, it will be used to track your experiment")
    set_cache("CURRENT_EXPERIMENT", experiment_id)

    with WebSocketClient(
        f"/log/{experiment_id}/",
        cred,
    ) as ws:
        runner = Runner(
            base_dir=train_file.parent,
            client=client,
            ws=ws,
            experiment_id=experiment_id,
        )
        do_review = typing_prompt(
            "\nDo you want me to review your code?",
            default="y",
            type=click.Choice(["y", "n"]),
            color="blue",
            keywords=["review"],
        )
        if do_review == "y":
            print_line(new_line_direction="up")
            typing_print("Code Review Results\n", color="blue", keywords=["Code Review Results"])
            runner.request_code_review()
            print_line(new_line_direction="up")
            typing_print("Code review is finished", color="blue", keywords=["Code review is finished"])

            confirm_review = typing_prompt(
                "\nDo you want to train with current setup?",
                default="y",
                type=click.Choice(["y", "n"]),
                color="blue",
                keywords=["train"],
            )
            if confirm_review == "n":
                typing_print("Okay, bye bye and see you next time!", color="blue", keywords=["bye bye"])
                return

        typing_print(
            "Generating modified training script to apply your settings...", color="blue", keywords=["modified"]
        )
        print_line(new_line_direction="down")
        typing_print("Modified training code\n", color="blue", keywords=["Modified training code"])

        excution_code = runner.request_generate_code()
        print_line(new_line_direction="both")
        if excution_code:
            typing_print(
                "I've modified the training code according to your settings!",
                color="blue",
                keywords=["modified the training code", "your settings"],
            )
            typing_print(
                "Let's start training! If anomaly is detected, I'll notify you via email. \n",
                color="blue",
                keywords=["anomaly is detected", "notify you via email"],
            )
            print_line(new_line_direction="down")
            runner.execute_train(excution_code)
        else:
            typing_print("Failed to generate code", color="red", keywords=["Failed to generate code"])
            typing_print("Training finished", color="red", keywords=["Training finished"])
