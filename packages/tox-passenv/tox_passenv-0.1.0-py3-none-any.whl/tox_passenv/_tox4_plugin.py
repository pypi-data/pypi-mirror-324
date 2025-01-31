import logging
import os

from tox.plugin import impl


logger = logging.getLogger(__name__)


@impl
def tox_add_env_config(env_conf, state):
    if not all(
        (
            passenv := os.environ.get("TOX_TESTENV_PASSENV", None),
            "runner" in env_conf,  # only tests environments
        )
    ):
        return

    env_values = [x for x in passenv.split() if x]
    if env_values:
        logger.info(
            "passing additional environment variables for test env %s: %s",
            env_conf.env_name,
            ", ".join(env_values),
        )
        env_conf["pass_env"].extend(env_values)
