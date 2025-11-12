from PySide6 import QtCore, QtWidgets

from trivox_conductor.common.logger import logger
from trivox_conductor.core.session.session_manager import SessionManager
from trivox_conductor.core.ui.nav_registry import ViewDescriptor, ViewRegistry
from trivox_conductor.ui.common.base_window_controller import (
    BaseWindowController,
)
from trivox_conductor.ui.common.controllers_mediator import ControllersMediator
from trivox_conductor.ui.views.main_window_view import MainWindowView
from trivox_conductor.ui.widgets.dashboard.quick_actions import (
    QuickActionsWidget,
)
from trivox_conductor.ui.widgets.dashboard.recorder_session import (
    RecorderSessionWidget,
)
from trivox_conductor.ui.widgets.dashboard.simple_card import SimpleCard


# optional: feature checks
def _has_capture_adapter() -> bool:
    try:
        from trivox_conductor.core.registry.capture_registry import (
            CaptureRegistry,
        )

        # adapt to your real API:
        return bool(
            getattr(CaptureRegistry, "get_active", None)
            and CaptureRegistry.get_active()
        ) or bool(
            getattr(CaptureRegistry, "all", None) and CaptureRegistry.all()
        )
    except Exception:
        return False


def _has_watcher() -> bool:
    try:
        from trivox_conductor.core.registry.watcher_registry import (
            WatcherRegistry,
        )

        return bool(
            getattr(WatcherRegistry, "get_active", None)
            and WatcherRegistry.get_active()
        ) or bool(
            getattr(WatcherRegistry, "all", None) and WatcherRegistry.all()
        )
    except Exception:
        return False


class MainWindowController(BaseWindowController):
    """
    Main window controller

    :extends: BaseWindowController
    """

    def __init__(self, mediator: ControllersMediator):
        """
        :param mediator: The controllers mediator
        :type mediator: ControllersMediator
        """
        super().__init__(mediator)
        self._window = MainWindowView()
        self._context = self._build_view_context()
        self._view_rows: dict[int, int] = {}  # nav row -> stack index

        self._setup_dashboard_cards()
        self._setup_dynamic_views()
        self.__connect_signals()

    def _build_view_context(self) -> dict:
        """
        Build the shared context dict passed into each view factory.
        You can extend this as needed.
        """
        return {
            "session_manager": SessionManager(),
            "pipeline_profile": None,  # later: current profile if GUI selects it
            # add more stuff here if views need it
        }

    def _setup_dashboard_cards(self) -> None:
        w = self._window

        # Quick Actions (only show if we have any capture adapter)
        qa_layout = QtWidgets.QVBoxLayout(w.quick_actions)
        qa_layout.setContentsMargins(0, 0, 0, 0)
        qa_layout.setSpacing(0)
        has_capture = _has_capture_adapter()
        if has_capture:
            qa = QuickActionsWidget(
                context=self._context, parent=w.quick_actions
            )
            qa_layout.addWidget(qa)
            w.quick_actions.setVisible(True)
        else:
            w.quick_actions.setVisible(False)

        # Recorder & Session (visible if capture is meaningful; else hide)
        rs_layout = QtWidgets.QVBoxLayout(w.recorder_and_session)
        rs_layout.setContentsMargins(0, 0, 0, 0)
        rs_layout.setSpacing(0)
        if has_capture:
            rs = RecorderSessionWidget(
                context=self._context, parent=w.recorder_and_session
            )
            rs_layout.addWidget(rs)
            w.recorder_and_session.setVisible(True)
        else:
            w.recorder_and_session.setVisible(False)

        # Pipeline Queue (nothing yet; show a label or hide entirely)
        pq_layout = QtWidgets.QVBoxLayout(w.pipeline_queue)
        pq_layout.setContentsMargins(0, 0, 0, 0)
        pq_layout.setSpacing(0)
        # for now: simple placeholder label; change to False to hide
        pq = SimpleCard(
            title="Pipeline Queue",
            body="(coming soon)",
            parent=w.pipeline_queue,
        )
        pq_layout.addWidget(pq)
        w.pipeline_queue.setVisible(True)

        # Replay Watch (on/off; for now label based on watcher existence)
        rw_layout = QtWidgets.QVBoxLayout(w.replay_watch)
        rw_layout.setContentsMargins(0, 0, 0, 0)
        rw_layout.setSpacing(0)
        has_watch = _has_watcher()
        rw = SimpleCard(
            title="Replay / Watch",
            body="Watcher available" if has_watch else "Watcher not available",
            parent=w.replay_watch,
        )
        rw_layout.addWidget(rw)
        w.replay_watch.setVisible(True)  # keep visible with status label

        # Recent Outputs (placeholder)
        ro_layout = QtWidgets.QVBoxLayout(w.recent_outputs)
        ro_layout.setContentsMargins(0, 0, 0, 0)
        ro_layout.setSpacing(0)
        ro = SimpleCard(
            title="Recent Outputs",
            body="(coming soon)",
            parent=w.recent_outputs,
        )
        ro_layout.addWidget(ro)
        w.recent_outputs.setVisible(True)

        # System Health (placeholder)
        sh_layout = QtWidgets.QVBoxLayout(w.system_health)
        sh_layout.setContentsMargins(0, 0, 0, 0)
        sh_layout.setSpacing(0)
        sh = SimpleCard(
            title="System Health", body="(coming soon)", parent=w.system_health
        )
        sh_layout.addWidget(sh)
        w.system_health.setVisible(True)

    def _setup_dynamic_views(self) -> None:
        """
        - Clear navList and recreate entries.
        - Keep Dashboard (stack index 0).
        - Add one entry per registered "main" view.
        """
        nav = self._window.navList
        stack = self._window.stack

        nav.clear()
        self._view_rows.clear()

        # --- Dashboard as static entry ---
        dashboard_index = stack.indexOf(self._window.pageDashboard)
        if dashboard_index == -1:
            dashboard_index = 0

        dash_item = QtWidgets.QListWidgetItem("Dashboard")
        dash_item.setData(QtCore.Qt.UserRole, dashboard_index)
        nav.addItem(dash_item)
        self._view_rows[0] = dashboard_index

        # --- Dynamic main views ---
        descriptors = [
            d
            for d in ViewRegistry.all().values()
            if d.area == "main" and self._is_view_visible(d)
        ]
        descriptors.sort(key=lambda d: d.order)

        for desc in descriptors:
            widget = desc.factory(context=self._context)
            idx = stack.addWidget(widget)

            item = QtWidgets.QListWidgetItem(desc.title)
            item.setData(QtCore.Qt.UserRole, idx)
            row = nav.count()
            nav.addItem(item)
            self._view_rows[row] = idx

        nav.setCurrentRow(0)
        stack.setCurrentIndex(dashboard_index)

    def _is_view_visible(self, desc: ViewDescriptor) -> bool:
        """
        Decide if a descriptor should be shown based on the current context.
        """
        if desc.visible_if is None:
            return True

        try:
            return bool(desc.visible_if(self._context))
        except Exception:  # don't break the GUI if a condition explodes
            logger.exception(
                "Error evaluating visibility for view %s", desc.id
            )
            return False

    def __connect_signals(self):
        """
        This function connects signals to slots.
        """
        self._window.navList.currentRowChanged.connect(
            self._on_nav_row_changed
        )

    def _on_nav_row_changed(self, row: int) -> None:
        """
        When user selects an item in the nav list, switch the stacked widget.
        """
        idx = self._view_rows.get(row)
        if idx is None:
            return
        self._window.stack.setCurrentIndex(idx)

    def show(self):
        logger.info("Showing Main Window")
        self._window.show()
