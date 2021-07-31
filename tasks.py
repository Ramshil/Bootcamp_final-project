from flask import render_template, request, redirect, url_for,g,Blueprint
from . import db
import datetime

bp = Blueprint("tasks", "tasks", url_prefix="/tasks")

@bp.route("/")
def alltasks():
    conn = db.get_db() 
    cursor = conn.cursor()
    
    cursor.execute("select week_day from task")
    taskdays = cursor.fetchall()
    for taskday in taskdays:
     today = datetime.datetime.now().strftime("%A")
     week_days=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
     if week_days.index(today)>week_days.index(taskday[0]):
       cursor.execute("update task set status=%s where week_day=%s and status=%s", ("Overdue",taskday[0],"Due")) 
       conn.commit()
     if week_days.index(today)<week_days.index(taskday[0]):
       cursor.execute("update task set status=%s where week_day=%s and status=%s", ("Due",taskday[0],"Overdue")) 
       conn.commit()
     if week_days.index(today)==week_days.index(taskday[0]):
       current_time = datetime.datetime.now().strftime("%H")
       current_time_hour = int(current_time.split(":")[0])
       cursor.execute("select event_time_hours from task where week_day=%s",(taskday[0],))
       event_time_hours= cursor.fetchall()
       for event_time_hour in event_time_hours:
        if current_time_hour >event_time_hour[0]:
         cursor.execute("update task set status=%s where week_day=%s  and status=%s and event_time_hours=%s", ("Overdue",taskday[0],"Due",event_time_hour[0]))
         conn.commit()
        if current_time_hour <event_time_hour[0]:
         cursor.execute("update task set status=%s where week_day=%s  and status=%s and event_time_hours=%s", ("Due",taskday[0],"Overdue",event_time_hour[0]))
         conn.commit()
        if current_time_hour ==event_time_hour[0]:
          current_time = datetime.datetime.now().strftime("%H:%M")
          current_time_minute = int(current_time.split(":")[1])
          cursor.execute("select event_time_minutes from task where week_day=%s and event_time_hours=%s",(taskday[0],event_time_hour[0]))
          event_time_minutes= cursor.fetchall()
          for event_time_minute in event_time_minutes:
           if current_time_minute>event_time_minute[0]:
             cursor.execute("update task set status=%s where week_day=%s  and status=%s and event_time_hours=%s and event_time_minutes=%s", ("Overdue",taskday[0],"Due",event_time_hour[0],event_time_minute[0]))
             conn.commit()
           if current_time_minute<event_time_minute[0]:
             cursor.execute("update task set status=%s where week_day=%s  and status=%s and event_time_hours=%s and event_time_minutes=%s", ("Due",taskday[0],"Overdue",event_time_hour[0],event_time_minute[0]))
             conn.commit()
       
    cursor.execute("select * from task order by id asc")
    tasks = cursor.fetchall() 
    cursor.execute("select count(*) from task")
    count = cursor.fetchone()[0]
    cursor.execute("select count(*) from task where status=%s",("Due",))
    Due = cursor.fetchone()[0]
    cursor.execute("select count(*) from task where status=%s",("Overdue",))
    Overdue = cursor.fetchone()[0]
    cursor.execute("select count(*) from task where status=%s",("Done",))
    Done = cursor.fetchone()[0]
    return render_template("tasks/taskslist.html", tasks = tasks,Due=Due,Overdue=Overdue,count=count,Done=Done) 



@bp.route("/add", methods=["GET", "POST",])
def add_task(): 
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select * from task")
    tasks = cursor.fetchall() 
    cursor.execute("select count(*) from task")
    count = cursor.fetchone()[0]
    cursor.execute("select count(*) from task where status=%s",("Due",))
    Due = cursor.fetchone()[0]
    cursor.execute("select count(*) from task where status=%s",("Overdue",))
    Overdue = cursor.fetchone()[0]
    cursor.execute("select count(*) from task where status=%s",("Done",))
    Done = cursor.fetchone()[0]
    
    if request.method == "GET":
        week_days=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        return render_template("tasks/taskadd.html",week_days=week_days,count=count,Due=Due,Overdue=Overdue,Done=Done)
    elif request.method == "POST":
        day = request.form.get("day")
        name = request.form.get("name")
        Time_hours= request.form.get("Time_hours")
        Time_minutes= request.form.get("Time_minutes")
        cursor.execute("INSERT INTO task(name,week_day,event_time_hours,event_time_minutes,status) VALUES (%s,%s,%s,%s,%s)",(name,day,Time_hours,Time_minutes,"Due"))
        conn.commit()
        return redirect(url_for("tasks.alltasks"), 302)


    @bp.route("/<id>/edit", methods=["GET", "POST",])
def edit_task(id): 
    conn = db.get_db()
    cursor = conn.cursor()
    
    if request.method == "GET":
        cursor.execute("select name,week_day,event_time_hours,event_time_minutes,status from task where id = %s", (id,))
        name,day,Time_hours,Time_minutes,status = cursor.fetchone()
        week_days=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        statuses=["Due","Overdue","Done"]
        cursor.execute("select * from task")
        tasks = cursor.fetchall() 
        cursor.execute("select count(*) from task")
        count = cursor.fetchone()[0]
        cursor.execute("select count(*) from task where status=%s",("Due",))
        Due = cursor.fetchone()[0]
        cursor.execute("select count(*) from task where status=%s",("Overdue",))
        Overdue = cursor.fetchone()[0]
        cursor.execute("select count(*) from task where status=%s",("Done",))
        Done = cursor.fetchone()[0]
        return render_template("tasks/taskedit.html",name=name,day=day,Time_hours=Time_hours,Time_minutes=Time_minutes,id=id,week_days=week_days,statuses=statuses,status=status,count=count,Due=Due,Overdue=Overdue,Done=Done)
    elif request.method == "POST":
        status = request.form.get("Status")
        day = request.form.get("day")
        name = request.form.get("name")
        Time_hours= request.form.get("Time_hours")
        Time_minutes= request.form.get("Time_minutes")
        cursor.execute("update task set name = %s, week_day=%s , event_time_hours=%s,event_time_minutes=%s,status=%s where id=%s", (name, day,Time_hours,Time_minutes,status,id))
        conn.commit()
        return redirect(url_for("tasks.alltasks"), 302)
        

@bp.route("/Due")
def due_task(): 
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
    cursor.execute("select * from task where status=%s",("Due",))
    tasks_due = cursor.fetchall() 
    return render_template("tasks/taskdue.html", tasks_due = tasks_due,count=count,Due=Due,Overdue=Overdue,Done=Done) 


@bp.route("/Overdue")
def overdue_task(): 
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
    cursor.execute("select * from task where status=%s",("Overdue",))
    tasks_overdue = cursor.fetchall() 
    return render_template("tasks/taskoverdue.html", tasks_overdue = tasks_overdue,count=count,Due=Due,Overdue=Overdue,Done=Done) 



@bp.route("/done")
def done_task(): 
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
    cursor.execute("select * from task where status=%s",("Done",))
    tasks_done = cursor.fetchall() 
    return render_template("tasks/taskdone.html", tasks_done = tasks_done,count=count,Due=Due,Overdue=Overdue,Done=Done) 




