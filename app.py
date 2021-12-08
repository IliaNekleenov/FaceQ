from config import app, database_manager
from flask import request


@app.route('/all')
def hello_world():
    return str(database_manager.select_all())


@app.route('/enq')
def enq():
    face_metrics = request.args.get('metrics')
    database_manager.enqueue_by_metrics(face_metrics)
    return str([x for x in database_manager.select_all()])


@app.route('/next')
def take_next():
    ticket_number = database_manager.take_first()
    return str(ticket_number)


if __name__ == '__main__':
    app.run()
