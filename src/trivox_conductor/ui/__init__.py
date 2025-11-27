from trivox_conductor.common.logger import logger
from trivox_conductor.ui.app import TrivoxInspectorApp


def run_gui(**kwargs):
    """
    Run the GUI.
    """
    logger.debug("Starting GUI with kwargs: %s", kwargs)
    # ---- validate kwargs BEFORE touching Qt ----
    allowed = {"verbose", "pipeline_profile"}
    unexpected = set(kwargs) - allowed
    if unexpected:
        # match Python's style for unexpected kwargs
        bad = ", ".join(sorted(unexpected))
        raise TypeError(f"run_gui() got unexpected keyword argument(s): {bad}")

    app = TrivoxInspectorApp(**kwargs)
    app.run()
