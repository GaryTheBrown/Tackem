'''Base for the backend'''
from abc import ABCMeta, abstractmethod
import threading
from libs.database.table import Table
from libs.database.messages.sql_message import SQLMessage
from libs.exceptions import TableCheckFailure

class BackendBase(metaclass=ABCMeta):
    '''Base for the backend'''

    __event_lock = threading.Event()
    __event_list = []
    __event_list_lock = threading.Lock()

    __thread_run = True

    __conn = None

    def __init__(self):
        '''INIT'''
        self.__thread = threading.Thread(target=self.__run, args=())
        self.__thread.setName("DATABASE")


    def start_thread(self) -> bool:
        '''start the thread'''
        if not self.__thread.is_alive():
            self.__thread.start()
            return True
        return False

    def stop_thread(self):
        '''stop the thread'''
        if self.__thread.is_alive():
            self.__thread_run = False
            self.__event_lock.set()
            self.__thread.join()

    def get_thread_run(self) -> bool:
        '''return if thread is running'''
        return self.__thread.is_alive()


##################
##USER FUNCTIONS##
##################
    def call(self, message: SQLMessage):
        '''function to pass the query/table through to the backend thread'''
        if not isinstance(message, SQLMessage):
            return None
        with self.__event_list_lock:
            self.__event_list.append(message)
        message.event_wait()

##########
##THREAD##
##########
    def __run(self):
        '''Threadded Run'''
        self.__startup()
        while self.__thread_run:
            self.__run_loop()
        self.__shutdown()

    def __run_loop(self):
        '''run commands'''
        self.__event_lock.wait()
        while self.__event_list:
            with self.__event_list_lock:
                job = self.__event_list.pop()
            if isinstance(job, SQLMessage):
                self.__run_message_action(job)
            else:
                print("WTF IS PASSED IN???", type(job), job)
        self.__event_lock.clear()

    def __run_message_action(self, job: SQLMessage):
        if isinstance(job.action, Table):
            if self.__table_check(job.action):
                job.event_set()
            else:
                raise TableCheckFailure
        else:
            self.__do_job(job)

    def __do_job(self, job: SQLMessage):
        '''do the magic work for each job'''
        cursor = self.__get_cursor()
        if job.query_vars:
            cursor.execute(job.query, job.query_vars)
        else:
            cursor.execute(job.query)
        self.__conn.commit()

        data = cursor.fetchall()
        if len(data) == 1:
            job.return_data = data.pop()
            return
        job.return_data = data

    @abstractmethod
    def __startup(self):
        '''Setup the System Here'''

    @abstractmethod
    def __shutdown(self):
        '''Shutdown the System Here'''

    @abstractmethod
    def __get_cursor(self):
        '''returns a sql cursor'''

    @abstractmethod
    def __table_check(self, table: Table) -> bool:
        '''Check, Create or Update Table in DB.'''
