from flet.core.control import Control


class OneSignal(Control):
    def __init__(self, app_id: str):
        super().__init__()
        self.app_id = app_id

    def _get_control_name(self):
        return "onesignal_flet"

    def _before_build_command(self):
        self._set_attr("appId", self.app_id)