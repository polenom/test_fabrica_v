from celery import shared_task

@shared_task
def bar():
    print('heloooooooooooooow')
    return "Helllow"