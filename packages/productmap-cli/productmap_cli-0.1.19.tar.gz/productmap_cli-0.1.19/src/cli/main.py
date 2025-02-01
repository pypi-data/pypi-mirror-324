import click

from cli.pmcli import generate_map, validate_file


@click.command()
@click.version_option()
@click.pass_context
@click.argument("url")
@click.argument("nickname")
@click.argument("email")
@click.option("--action", type=click.Choice(["validate", "generate"]), required=True)
def main(
        ctx: click.Context,
        url: str,
        nickname: str,
        email: str,
        action: str,
):
    """
        CLI for validating and generating maps for files using the ProductMap API.
        """
    if url is None:
        ctx.fail("File URL is required")
    if nickname is None:
        ctx.fail("Nickname is required")
    if email is None:
        ctx.fail("Email is required")

    try:
        if action == "validate":
            result = validate_file(ctx, url, nickname, email)
            click.echo(result)
        elif action == "generate":
            result = generate_map(ctx, url, nickname, email)
            click.echo(result)
    except click.ClickException as e:
        ctx.fail(f"Operation failed: {e}")


if __name__ == "__main__":
    main()
