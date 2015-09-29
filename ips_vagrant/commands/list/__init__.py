import click
from ips_vagrant.cli import pass_context, Context
from ips_vagrant.common import domain_parse
from ips_vagrant.models.sites import Domain, Site, Session


# noinspection PyUnboundLocalVariable
@click.command('list', short_help='List all domains, or all installations under a specified <domain>.')
@click.argument('dname', default=False, metavar='<domain>')
@click.argument('site', default=False, metavar='<site>')
@pass_context
def cli(ctx, dname, site):
    """
    List all domains if no <domain> is provided. If <domain> is provided but <site> is not, lists all sites
    hosted under <domain>. If both <domain> and <site> are provided, lists information on the specified site.
    """
    assert isinstance(ctx, Context)

    if dname:
        dname = domain_parse(dname).hostname
        domain = Session.query(Domain).filter(Domain.name == dname).first()

        # No such domain
        if not domain:
            click.secho('No such domain: {dn}'.format(dn=dname), fg='red', bold=True, err=True)
            return

    if site:
        site = Site.get(domain, site)
        if not site:
            click.secho('No such site: {site}'.format(site=site), fg='red', bold=True, err=True)

        click.secho('Name: {n}'.format(n=site.name), bold=True)
        click.secho('Domain: {dn}'.format(dn=site.domain.name), bold=True)
        click.secho('Version: {v}'.format(v=site.version), bold=True)
        click.secho('IN_DEV: {id}'.format(id='Enabled' if site.in_dev else 'Disabled'), bold=True)
        click.secho('License Key: {lk}'.format(lk=site.license_key), bold=True)
        click.secho('SSL: {s}'.format(s='Enabled' if site.ssl else 'Disabled'), bold=True)
        click.secho('SPDY: {s}'.format(s='Enabled' if site.spdy else 'Disabled'), bold=True)
        click.secho('GZIP: {g}'.format(g='Enabled' if site.gzip else 'Disabled'), bold=True)
        return

    # Print sites
    if dname:
        # Get sites
        sites = Site.all(domain)
        if not sites:
            click.secho('No sites active under domain: {dn}'.format(dn=dname), fg='red', bold=True, err=True)
            return

        # Display site data
        for site in sites:
            prefix = '[DEV] ' if site.in_dev else ''
            click.secho('{pre}{name} ({ver})'.format(pre=prefix, name=site.name, ver=site.version), bold=True)

        return

    # Print domains
    domains = Domain.all()
    for domain in domains:
        # Extra domains
        extras = ''
        if domain.extras:
            extras = ' ({dnames})'.format(dnames=str(domain.extras).replace(',', ', '))

        click.secho('{dname}{extras}'.format(dname=domain.name, extras=extras), bold=True)
