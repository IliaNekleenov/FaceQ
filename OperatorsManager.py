from multiprocessing import Queue
from time import sleep

import Logger
from DatabaseManager import DatabaseManager
import socket

database_manager = DatabaseManager(drop_if_exists=False)

operators_hosts = {}
sockets: {int: socket.socket} = {}


def process_operators(enqueue_events: Queue, logger: Logger):
    logger.info('starting processing operators')
    while True:
        try:
            refresh_operators(logger)
            for operator_id, sock in sockets.items():
                if sock is None:
                    sockets[operator_id] = create_connection(operators_hosts[operator_id], logger)
                logger.debug('sending 0')
                sock.sendall('0'.encode('utf-8'))
                logger.debug('sent 0, receiving response')
                data = readline(sock)
                logger.debug(f'received response: {str(data)}')
                if data and data[0] == '1':
                    if enqueue_events.empty():
                        logger.debug('queue is empty')
                        sock.sendall('10000'.encode('utf-8'))
                    else:
                        ticket_number = enqueue_events.get()
                        logger.info(f'set ticket_number={ticket_number} to operator_id={operator_id}')
                        sock.sendall(str(ticket_number).encode('utf-8'))
                        database_manager.update_operator_ticket_number(operator_id, ticket_number)
        except Exception as e:
            logger.error(f'exception while processing operators: {str(e)}')
        sleep(1)


def refresh_operators(logger: Logger):
    logger.debug('refreshing operators')
    operators = database_manager.select_operators()
    logger.debug(f'operators: {operators}')
    for operator_id, operator_host, ticket_number in operators:
        logger.debug(f'operator id: {operator_id}')
        if operators_hosts.get(operator_id) != operator_host:
            logger.debug(f'new host: {operator_host}')
            operators_hosts[operator_id] = operator_host
            if sockets.get(operator_id) is not None:
                try:
                    sockets[operator_id].close()
                except Exception:
                    pass
            sockets[operator_id] = create_connection(operator_host, logger)


def create_connection(host, logger: Logger):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, 80))
        sock.settimeout(10)

        logger.info(f'connected to operator: {host}')
        return sock
    except Exception:
        logger.error(f'could not connect to operator: {host}')
        return None


def readline(sock: socket):
    result = ""
    while not result.endswith('\n'):
        result += sock.recv(1).decode('utf-8')
    return result
