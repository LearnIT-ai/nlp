from AI_router import ai_access
from default_router import default_router
class RouteRegistrator:
    def __init__(self, app):
        self.app = app

    def register_all(self):
        self.app.include_router(ai_access)
        self.app.include_router(default_router)
        return self.app
