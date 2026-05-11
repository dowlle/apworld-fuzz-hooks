from fuzz import BaseHook
from worlds import AutoWorldRegister
import worlds
import os
import tempfile


def refresh_netdata_package():
    for world_name, world in AutoWorldRegister.world_types.items():
        if world_name not in worlds.network_data_package["games"]:
            worlds.network_data_package["games"][world_name] = world.get_data_package_data()


class Hook(BaseHook):
    """Pairs the apworld-under-test with the `Empty` world in every generation,
    catching cross-world interaction bugs (the UT-style check).

    Requires the `Empty` apworld (https://github.com/Eijebong/empty-apworld)
    to already be registered. Callers pre-place `empty.apworld` in the AP
    install's `custom_worlds/` folder before invoking fuzz.py.
    """

    def setup_main(self, args):
        self._tmp = tempfile.TemporaryDirectory(prefix="apfuzz")
        with open(os.path.join(self._tmp.name, "empty.yaml"), "w") as fd:
            fd.write("""
name: Player{number}
description: Empty world to weed restrictive starts out
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
        refresh_netdata_package()
