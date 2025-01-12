from AI_router import ai_access

class RouteRegistrator:
    def __init__(self, app):
        self.app = app

    def register_all(self):
        self.app.include_router(ai_access)
        return self.app
