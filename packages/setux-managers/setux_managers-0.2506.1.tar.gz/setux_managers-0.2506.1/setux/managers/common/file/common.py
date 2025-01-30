from pathlib import Path

from setux.core.manage import SpecChecker


class PathChecker(SpecChecker):
    def fetch(self, key, *args, **spec):
        key = str(key) if isinstance(key, Path) else key
        return super().fetch(key, *args, **spec)

    def __bool__(self):
        return bool(self.get())

