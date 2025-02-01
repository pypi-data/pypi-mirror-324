from pathlib import Path

from setux.core.manage import Manager
from setux.logger import debug, info, error, green, yellow, red


class Distro(Manager):
    '''Python venv management
    '''
    manager = 'venv'
    rc = Path('~/.bashrc').expanduser()
    venv_path = Path('~/venv').expanduser()
    venv_name = 'setux'

    def get_path(self, name):
        return self.target.dir.fetch(self.venv_path / name)

    @property
    def current(self):
        ret, out, err = self.run('which python')
        full = out[0]
        if full.startswith(str(self.venv_path)):
            venv = full.split('/')[-3]
            return venv

    @property
    def current_path(self, name):
        if self.current:
            return self.get_path(self.current)

    def reset(self, name=None):
        found = self.get_path(name) if name else self.current_path
        if found:
            found.remove()

    def create(self, name):
        self.reset(name)
        ret, out, err = self.target.run(f'mkdir -p {self.venv_path}')
        ret, out, err = self.target.run(f'python -m venv {self.venv_path}/{name}')

    def activate(self, name=None):
        name = name or self.venv_name
        if self.current == name:
            return True

        with yellow(f'   activate {name}'):
            found = self.get_path(name)
            if not found:
                self.create(name)
                found = self.get_path(name)
            if found:
                ok = self.target.deploy('upd_cfg',
                    path = self.rc,
                    select = 'activate',
                    line = f'source {found.key}/bin/activate',
                    report = 'quiet',
                )
            else:
                error(f'VENV "{name}" not found')
                ok = False

        if ok:
            green(f'   {name} activated')
        else:
            red(f'   venv {name}')
        return ok

    def deactivate(self):
        self.target.deploy('upd_cfg',
            path = self.rc,
            remove = 'activate',
        )

