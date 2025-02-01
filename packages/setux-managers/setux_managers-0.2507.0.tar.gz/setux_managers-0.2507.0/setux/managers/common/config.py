from pybrary import Config

from setux.core.manage import Manager


default_script_header = '''
    #!/bin/bash
    shopt -s expand_aliases
    set -e
'''


class Distro(Manager):
    '''Setux Config management
    '''
    manager = 'config'
    config = Config('setux')

    @property
    def script_header(self):
        return self.config.script_header or default_script_header

    def __getattr__(self, name):
        return getattr(self.config, name)
