DROP TABLE IF EXISTS time cascade;
DROP TABLE IF EXISTS task cascade;


CREATE TABLE time (
       id serial primary key,
       time_of_event serial UNIQUE NOT NULL
       );
    


CREATE TABLE task (
       id serial primary key,
       name TEXT NOT NULL ,
       week_day TEXT,
       event_time_hours serial,
       event_time_minutes serial,
       status TEXT
);      



