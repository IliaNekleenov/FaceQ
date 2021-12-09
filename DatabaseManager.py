import sqlite3


class DatabaseManager:
    def __init__(self, database_name='queue.db', drop_if_exists=True):
        self.connection = sqlite3.connect(database_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        if drop_if_exists:
            self.drop_database()
        self.create_database()

    def drop_database(self):
        self.cursor.execute("""
        drop table if exists operators
        """)
        self.cursor.execute("""
        drop table if exists faceq_persons
        """)
        self.connection.commit()

    def create_database(self):
        self.cursor.execute("""
        create table if not exists operators (
            id integer primary key,
            host text not null,
            ticket_number integer)
        """)
        self.cursor.execute("""
        create table if not exists faceq_persons (
            id integer primary key, 
            face_metrics text not null,
            ticket_number integer,
            visits_count integer not null)
        """)
        self.connection.commit()

    def select_all(self):
        self.cursor.execute("""
        select * from faceq_persons
        """)
        return self.cursor.fetchall()

    def enqueue_by_id(self, person_id: int):
        ticket_number = self.__find_max_ticket_number() + 1
        self.cursor.execute("""
        update faceq_persons
        set ticket_number = ?,
            visits_count = visits_count + 1
        where id = ?
        """, (ticket_number, person_id))

    def enqueue_by_metrics(self, face_metrics_string):
        ticket_number = self.__find_max_ticket_number() + 1
        self.cursor.execute("""
        insert into faceq_persons (face_metrics, ticket_number, visits_count) values (?, ?, ?)
        """, (face_metrics_string, ticket_number, 1))
        self.cursor.execute("""
        select last_insert_rowid()
        """)
        inserted_person_id = int(self.cursor.fetchone()[0])
        self.connection.commit()
        return inserted_person_id, ticket_number

    def __find_max_ticket_number(self):
        self.cursor.execute("""
        select max(ticket_number) from faceq_persons
        """)
        result = self.cursor.fetchone()
        print(f"select max ticket number: {result}")
        if result[0] is None:
            return 0
        return int(result[0])

    def take_first(self):
        self.cursor.execute("""
        select min(ticket_number), id from faceq_persons
        """)
        min_ticket_number, person_id = self.cursor.fetchone()
        print(f"select max ticket number: {min_ticket_number} (id={person_id})")
        if min_ticket_number[0] is None:
            return None
        self.cursor.execute("""
        update faceq_persons
        set ticket_number = null
        where id = ?
        """, (int(min_ticket_number), person_id))
        self.connection.commit()
        return min_ticket_number

    def select_operators(self):
        self.cursor.execute("""
        select * from operators
        """)
        return self.cursor.fetchall()

    def update_operator_ticket_number(self, operator_id, ticket_number):
        self.cursor.execute("""
        update operators
        set ticket_number = ?
        where id = ?
        """, (ticket_number, operator_id))
        self.connection.commit()
