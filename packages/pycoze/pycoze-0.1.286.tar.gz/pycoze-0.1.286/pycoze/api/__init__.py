from .lib.window_cls import WindowCls
from .lib.tab_cls import TabCls

class Api:
    def __init__(self) -> None:
        self.window = WindowCls()
        self.tab = TabCls()

api = Api()
window = api.window
tab = api.tab

# from ps_view import ViewCls, WebsiteViewCls, FileViewCls, DirectoryViewCls, WorkflowCls