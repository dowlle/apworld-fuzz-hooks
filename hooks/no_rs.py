from fuzz import BaseHook
from worlds import AutoWorldRegister
import os
import tempfile


class Hook(BaseHook):
    """Adds an `Empty` player to every yaml-set so generation gets exercised
    even when an apworld would otherwise restrictive-start out of the room.

    Requires the `Empty` apworld (https://github.com/Eijebong/empty-apworld)
    to already be registered with AutoWorldRegister. Callers pre-place
    `empty.apworld` in the AP install's `custom_worlds/` folder before
    invoking fuzz.py, so AutoWorldRegister picks it up at import time.
    """

    def setup_main(self, args):
        self._tmp = tempfile.TemporaryDirectory(prefix="apfuzz")
        with open(os.path.join(self._tmp.name, "empty.yaml"), "w") as fd:
            fd.write("""
name: Player{number}
description: YAML used to weed out restrictive starts. Apworld can be found at https://github.com/Eijebong/empty-apworld
game: Empty
Empty: {}
            """)
        args.with_static_worlds = self._tmp.name

    def setup_worker(self, args):
        if 'Empty' not in AutoWorldRegister.world_types:
            raise RuntimeError(
                "The `empty` apworld needs to be present in the AP install's "
                "custom_worlds/ folder before fuzz.py starts. Get it from "
                "https://github.com/Eijebong/empty-apworld."
            )
