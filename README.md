
![](https://github.com/saasitive/dynamically-update-periodic-tasks/raw/main/media/banner.jpg)

# Dynamically update periodic tasks in Celery and Django

Example project showing how to dynamically add and remove periodic tasks in Celery and Django. It is using `PeriodicTask` class from [**`django-celery-beat`**](https://github.com/celery/django-celery-beat) package.

This example repository is very simple demo of [uptime monitoring service](https://monitor-uptime.com). User can add server address and interval at which server uptime status will be checked. Tasks can be dynamically added or removed.

You can read more about [dynamic periodic tasks in the article](https://saasitive.com/tutorial/dynamically-update-periodic-tasks-celery/).


## Sequence diagram of uptime monitoring 

```mermaid
sequenceDiagram
    actor U as User
    participant S as Server
    participant DB as Database
    participant B as Celery Beat
    participant W as Celery Worker
    
    U->>S: Create monitor 
    Note right of S: Create objects in DB
    S->>DB: Create Monitor object
    S->>DB: Create IntervalSchedule object
    S->>DB: Create Periodictack object
    
    loop every beat period
        DB->>B: Get info about periodic tasks
    end
    loop Every interval period
        B->>W: Create task
        Note right of W: Execute task
        W->>DB: Save task result (request data)
    end 
    
```
