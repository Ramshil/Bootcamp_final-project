import  random
from flask import Flask, render_template

def create_app():
    app = Flask("bootcamp_final_project")
    app.config.from_mapping(
        DATABASE="tasks"
    )
    
    from . import tasks 
    app.register_blueprint(tasks.bp)

    from . import db 
    db.init_app(app) 

    @app.route("/")
    def index():
        conn = db.get_db()
        curs = conn.cursor()
        curs.execute("select count(*) from task")
        count = curs.fetchone()[0]
        curs.execute("select count(*) from task where status=%s",("Overdue",))
        Overdue = curs.fetchone()[0]
        return render_template('index.html',count=count,Overdue=Overdue)


    return app
    
