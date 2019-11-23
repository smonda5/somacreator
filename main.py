import somacreator.builder as builder
import somacreator.const as const
import click


@click.command()
@click.option('--wsp', default='SAMPLE_WSP', help='Web Service Proxy Name, defaults to SAMPLE_WSP')
@click.option('--fsh', default='SAMPLE_FSH', help='Web Service Front Side Handler Name, defaults to SAMPLE_FSH')
@click.option('--domain', default='default', help='Datapower Domain Name, defaults to default')
def main(wsp, fsh, domain):
    path = const.INPUTLOCATION
    click.echo("\nBuilding SOMA ... \n")
    b = builder.SOMABuilder(path)
    b.build_soma(wsp, fsh, domain)


if __name__ == '__main__':
    main()
