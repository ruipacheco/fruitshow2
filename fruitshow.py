# -*- coding: utf-8 -*-

from flask_failsafe import failsafe

@failsafe
def create_app():
    from app import app
    app.config.from_object('config')
    app.run()
    
if __name__ == "__main__":
    create_app().run()