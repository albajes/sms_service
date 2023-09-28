from service2.celery import app


@app.task(name='my_sender.task.send_message', queue='data_queue', exchange='celery')
def send_message(sms, sender_id):
    pass
