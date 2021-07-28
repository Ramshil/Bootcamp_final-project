from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask import g
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
     now_day = datetime.datetime.now()
     today=now_day.strftime("%A")
     week_days=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
     if week_days.index(today)>week_days.index(taskday[0]):
       cursor.execute("update task set status=%s where week_day=%s and status=%s", ("Overdue",taskday[0],"Due"))
     if week_days.index(today)==week_days.index(taskday[0]):
       now_time = datetime.datetime.now()
       current_time = now_time.strftime("%H")
       x = current_time.split(":")
       x[0]=int(x[0])
       cursor.execute("select event_time_hours from task where week_day=%s",(taskday[0],))
       event_time_hours= cursor.fetchall()
       for time in event_time_hours:
        if x[0]>time[0]:
         cursor.execute("update task set status=%s where week_day=%s  and status=%s and event_time_hours=%s", ("Overdue",taskday[0],"Due",time[0]))
        if x[0]==time[0]:
          now_time = datetime.datetime.now()
          current_time = now_time.strftime("%H:%M")
          y = current_time.split(":")
          y[1]=int(y[1])
          cursor.execute("select event_time_minutes from task where week_day=%s and event_time_hours=%s",(taskday[0],time[0]))
          event_time_minutes= cursor.fetchall()
          for time_m in event_time_minutes:
           if y[1]>time_m[0]:
             cursor.execute("update task set status=%s where week_day=%s  and status=%s and event_time_hours=%s and event_time_minutes=%s", ("Overdue",taskday[0],"Due",time[0],time_m[0]))
       
    cursor.execute("select * from task")
    tasks = cursor.fetchall() 

    return render_template("tasks/taskslist.html", tasks = tasks) 



@bp.route("/add", methods=["GET", "POST",])
def add_task(): 
    conn = db.get_db()
    cursor = conn.cursor()
    
    if request.method == "GET":
        week_days=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        return render_template("tasks/taskadd.html",week_days=week_days)
    elif request.method == "POST":
        status = request.form.get("status")
        day = request.form.get("day")
        name = request.form.get("name")
        Time_hours= request.form.get("Time_hours")
        Time_minutes= request.form.get("Time_minutes")
        cursor.execute("INSERT INTO task(name,week_day,event_time_hours,event_time_minutes,status) VALUES (%s,%s,%s,%s,%s)",(name,day,Time_hours,Time_minutes,status))
        conn.commit()
        return redirect(url_for("tasks.alltasks"), 302)



@bp.route("/<id>/edit", methods=["GET", "POST",])
def edit_task(id): 
    conn = db.get_db()
    cursor = conn.cursor()
    
    if request.method == "GET":
        cursor.execute("select name,week_day,event_time_hours,event_time_minutes from task where id = %s", (id,))
        name,day,Time_hours,Time_minutes = cursor.fetchone()
        week_days=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        return render_template("tasks/taskedit.html",name=name,day=day,Time_hours=Time_hours,Time_minutes=Time_minutes,id=id,week_days=week_days)
    elif request.method == "POST":
        status = request.form.get("status")
        day = request.form.get("day")
        name = request.form.get("name")
        Time_hours= request.form.get("Time_hours")
        Time_minutes= request.form.get("Time_minutes")
        cursor.execute("update task set name = %s, week_day=%s ,status =%s , event_time_hours=%s,event_time_minutes=%s where id=%s", (name, day,status,Time_hours,Time_minutes,id))
        conn.commit()
        return redirect(url_for("tasks.alltasks"), 302)




