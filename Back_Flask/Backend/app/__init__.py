from flask import Flask


def register_router(flask_app: Flask):
    from router.auths.auths_router import auths_router

    from router.diary.diary_router import diary_router
    from router.stats.stats_router import report_router

    flask_app.register_blueprint(auths_router)
    flask_app.register_blueprint(diary_router)
    flask_app.register_blueprint(report_router)


def create_app():
    app = Flask(__name__)
    register_router(app)

    return app
