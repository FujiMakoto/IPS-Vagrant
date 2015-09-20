import os
import click
import logging
import pkgutil
import importlib
from ConfigParser import ConfigParser
from ips_vagrant.scraper import Login
from ips_vagrant.models.sites import DBSession

CONTEXT_SETTINGS = dict(auto_envvar_prefix='IPSV', max_content_width=100)


class Context(object):
    """
    CLI Context
    """
    def __init__(self):
        self.cookiejar = None
        self.config = ConfigParser()
        self.config_path = None
        self.log = None
        # self.license = None
        # self.cache = None
        self.database = NotImplemented
        self.basedir = os.path.join(os.path.dirname(os.path.realpath(__file__)))

        self.load_config(os.path.join(self.basedir, 'config', 'ipsv.conf'))
        self._login = None

    def setup(self):
        self._login = Login(self)

    @property
    def db(self):
        if self.database is NotImplemented:
            self.database = DBSession()

        return self.database

    def load_config(self, path):
        self.config_path = path
        self.config.read(self.config_path)

    def get_login(self, use_session=True):
        # Should we try and return an existing login session?
        if use_session and self._login.check():
            self.cookiejar = self._login.cookiejar
            return self.cookiejar

        # Prompt the user for their login credentials
        username = click.prompt('Username')
        password = click.prompt('Password', hide_input=True)
        remember = click.confirm('Save login session?', True)

        # Process the login
        cookiejar = self._login.process(username, password, remember)
        if remember:
            self.cookiejar = cookiejar

        return cookiejar

    def choice(self, opts, default=1, text='Please make a choice'):
        opts_len = len(opts)
        opts_enum = enumerate(opts, 1)
        opts = list(opts)

        for key, opt in opts_enum:
            click.echo('[{k}] {o}'.format(k=key, o=opt[1] if isinstance(opt, tuple) else opt))

        click.echo('-' * 12)
        opt = click.prompt(text, default, type=click.IntRange(1, opts_len))
        opt = opts[opt - 1]
        return opt[0] if isinstance(opt, tuple) else opt


# noinspection PyAbstractClass
class IpsvCLI(click.MultiCommand):
    """
    IPS Vagrant Commandline Interface
    """
    def list_commands(self, ctx):
        """
        List CLI commands
        @type   ctx:    Context
        @rtype: list
        """
        commands_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'commands')
        command_list = [name for __, name, ispkg in pkgutil.iter_modules([commands_path]) if ispkg]
        command_list.sort()
        return command_list

    def get_command(self, ctx, name):
        """
        Get a bound command method
        @type   ctx:    Context
        @param  name:   Command name
        @type   name:   str

        @rtype: object
        """
        try:
            # name = name.encode('ascii', 'replace')
            # mod = __import__('ips_vagrant.commands.cmd_' + name,
            #                  None, None, ['cli'])
            mod = importlib.import_module('ips_vagrant.commands.{name}'.format(name=name))
            return mod.cli
        except (ImportError, AttributeError):
            return


pass_context = click.make_pass_decorator(Context, ensure=True)


@click.command(cls=IpsvCLI, context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', count=True, default=1,
              help='-v|vv|vvv Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and '
                   '3 for debug')
@click.option('-c', '--config', type=click.Path(dir_okay=False, resolve_path=True),
              envvar='IPSV_CONFIG_PATH', default='/etc/ipsv/ipsv.conf', help='Path to the IPSV configuration file')
@pass_context
def cli(ctx, verbose, config):
    """
    IPS Vagrant Management Utility
    """
    assert isinstance(ctx, Context)
    # Set up the logger
    verbose = verbose if (verbose <= 3) else 3
    log_levels = {1: logging.WARN, 2: logging.INFO, 3: logging.DEBUG}
    log_level = log_levels[verbose]

    ctx.log = logging.getLogger('ipsv')
    ctx.log.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ctx.log.addHandler(ch)

    # Load the configuration
    if os.path.isfile(config):
        ctx.config_path = config
        ctx.log.debug('Loading configuration: %s', ctx.config_path)
        ctx.load_config(config)
    else:
        ctx.config_path = os.path.join(ctx.basedir, 'config', 'ipsv.conf')
        ctx.log.debug('Loading default configuration: %s', ctx.config_path)

    # ctx.license = license
    # ctx.cache = cache
    ctx.setup()
