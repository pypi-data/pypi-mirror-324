try:
    # tox4
    from tox.plugin import impl  # pylint: disable=unused-import
except ModuleNotFoundError:
    tox4 = False
else:
    tox4 = True


if tox4:
    # pylint: disable-next=unused-import
    from ._tox4_plugin import tox_add_env_config

__all__ = (
    "tox4",
    *(("tox_add_env_config",) if tox4 else ()),
)
