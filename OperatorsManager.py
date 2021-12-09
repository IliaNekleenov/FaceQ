from multiprocessing import Queue

import Logger
from DatabaseManager import DatabaseManager
import socket

database_manager = DatabaseManager()

operators_hosts = {}
operators_tickets = {}
sockets: {int: socket.socket} = {}
waiting_operators = set()


def process_operators(enqueue_events: Queue, logger: Logger):
    logger.info('starting processing operators')
    while True:
        try:
            refresh_operators(logger)
            for operator_id, sock in sockets.items():
                data = sock.recv(4)
                if data:
                    logger.info(f'operator_id={operator_id} is waiting new ticket number')
                    waiting_operators.add(operator_id)
                    database_manager.update_operator_ticket_number(operator_id, None)
                    operators_tickets.pop(operator_id)
                if operator_id in waiting_operators:
                    if not enqueue_events.empty():
                        ticket_number = enqueue_events.get()
                        logger.info(f'set ticket_number={ticket_number} to operator_id={operator_id}')
                        sock.sendall(ticket_number)
                        database_manager.update_operator_ticket_number(operator_id, ticket_number)
                        waiting_operators.remove(operator_id)
        except Exception as e:
            logger.error(f'exception while processing operators: {e}')


def refresh_operators(logger: Logger):
    operators = database_manager.select_operators()
    for operator_id, operator_host, ticket_number in operators:
        operators_tickets[operator_id] = ticket_number
        if operators_hosts[operator_id] != operator_host:
            operators_hosts[operator_id] = operator_host
            if sockets[operator_id] is not None:
                try:
                    sockets[operator_id].close()
                except:
                    pass
            sockets[operator_id] = create_connection(operator_host, logger)


def create_connection(host, logger: Logger):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, 5000))
        sock.settimeout(0.001)
        logger.info(f'connected to operator: {host}')
        return sock
    except Exception:
        logger.error(f'could not connect to operator: {host}')
        return None
