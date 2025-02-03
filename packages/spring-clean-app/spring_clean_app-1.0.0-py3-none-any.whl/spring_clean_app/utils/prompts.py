from typing import Any
import click

from spring_clean_app.utils.validators import Validator


def prompt_with_validator(prompt_mess, default_val, validator: Validator) -> Any:
    """Create prompt with validator"""
    while True:
        input_val = click.prompt(
            click.style(f"👉 {prompt_mess}", fg="bright_cyan"), default_val
        )
        if validator.validate(input_val):
            return input_val
        else:
            click.echo(validator.error_message)
