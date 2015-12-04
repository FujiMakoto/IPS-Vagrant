from ips_vagrant.installer.latest import Installer as Latest


version = (4, 1, 3, 2)


class Installer(Latest):

    def start(self):
        """
        Start the installation wizard
        """
        self.log.debug('Starting the installation process')
        self.system_check()
