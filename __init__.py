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
     cursor = conn.cursor()
     cursor.execute("select count(*) from task")
     count = cursor.fetchone()[0]
     cursor.execute("select count(*) from task where status=%s",("Due",))
     Due = cursor.fetchone()[0]
     cursor.execute("select count(*) from task where status=%s",("Overdue",))
     Overdue = cursor.fetchone()[0]
     cursor.execute("select count(*) from task where status=%s",("Done",))
     Done = cursor.fetchone()[0]
     return render_template("index.html", Due=Due,Overdue=Overdue,count=count,Done=Done) 

    return app
    
