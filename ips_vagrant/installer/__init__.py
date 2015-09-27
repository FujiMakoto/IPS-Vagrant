import importlib
import logging
from collections import OrderedDict
import os
import pkgutil


versions = OrderedDict()
path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
_modnames = [name for __, name, ispkg in pkgutil.iter_modules([path]) if not ispkg]
for modname in _modnames:
    m = importlib.import_module('ips_vagrant.installer.{name}'.format(name=modname))
    versions[getattr(m, 'version')] = getattr(m, 'Installer')
versions = OrderedDict(sorted(versions.items(), key=lambda v: v[0]))


def installer(cv, ctx, site):
    """
    Installer factory
    @param  cv: Current version (The version of IPS we are installing)
    @type   cv: tuple
    @return:    Installer instance
    @rtype:     ips_vagrant.installer.latest.Installer
    """
    log = logging.getLogger('ipsv.installer')
    log.info('Loading installer for IPS %s', cv)
    iv = None
    for v in versions:
        vstring = '.'.join(map(str, v)) if v else 'latest'
        cvstring = '.'.join(map(str, cv)) if cv else 'latest'
        log.debug('Checking if version %s is >= %s', vstring, cvstring)
        if (v is None) or (v >= cv):
            log.debug('Changing installer version to %s', vstring)
            iv = v

    log.info('Returning installer version %s', '.'.join(map(str, iv)) if iv else 'latest')
    return versions[iv](ctx, site)
