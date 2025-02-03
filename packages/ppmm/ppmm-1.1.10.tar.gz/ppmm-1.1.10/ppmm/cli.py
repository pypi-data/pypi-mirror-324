import click
from .config import (
    get_mirrors,
    get_current_mirror,
    add_mirror,
    remove_mirror,
    rename_mirror,
    test_mirrors,
    use_mirror,
    print_current_mirror,
    edit_mirrors
)


@click.group()
def cli():
    """Python Pip Mirror Manager"""
    pass


@cli.command()
def ls():
    """列出所有可用的镜像"""
    mirrors = get_mirrors()
    output_lines = []
    for name, url in mirrors.items():
        stars = "*" if url == get_current_mirror().stdout.strip() else " "
        stars = click.style(stars, fg="green")
        name += ' '
        output_lines.append(f"{stars} {name.ljust(14,'-')} {url}")
    click.echo("\n".join(output_lines))


@cli.command()
@click.argument("name")
def use(name):
    """切换到指定的镜像"""
    use_mirror(name)


@cli.command()
def test():
    """测试所有可用的镜像"""
    mirrors = get_mirrors()
    current = get_current_mirror().stdout.strip()
    key = next((key for key, val in mirrors.items() if val == current), None)
    results = test_mirrors()
    output_lines = []
    for name, time in results.items():
        stars = " "
        if name == key:
            stars = click.style("*", fg="green")
            time = click.style(time, bg="green")
        name += ' '
        output_lines.append(f"{stars} {name.ljust(14,'-')} {time}")
    click.echo("\n".join(output_lines))


@cli.command()
def current():
    """显示当前使用的镜像"""
    print_current_mirror()


@cli.command()
@click.argument("name")
@click.argument("url")
def add(name, url):
    """添加一个新的镜像"""
    add_mirror(name, url)


@cli.command()
@click.argument("name")
def rm(name):
    """删除一个已有的镜像"""
    remove_mirror(name)


@cli.command()
@click.argument("old_name")
@click.argument("new_name")
def rename(old_name, new_name):
    """重命名一个已有的镜像"""
    rename_mirror(old_name, new_name)

@cli.command()
@click.argument("name")
@click.argument("url")
def edit(name, url):
    """修改一个已有的镜像"""
    edit_mirrors(name, url)

@cli.command()
def help():
    """显示帮助信息"""
    help_text = """
    ppmm: Python Pip Mirror Manager
    Usage: mm <command>
        Commands:
        ls                              List all mirrors
        use <name>                      Switch to a specific mirror
        test                            Test all mirrors
        current                         Show current mirror
        add <name> <url>                Add a new mirror
        edit <name> <url>               Edit a mirror
        rm <name>                       Delete an existing mirror
        rename <old_name> <new_name>    Rename a mirror
        help                            Show this help message
    """
    click.echo(help_text)


if __name__ == "__main__":
    cli()
