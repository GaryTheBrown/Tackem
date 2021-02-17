'''Base for the backend'''
from abc import ABCMeta, abstractmethod
import threading
from libs.database.table import Table
from libs.database.messages.sql_message import SQLMessage
from libs.exceptions import TableCheckFailure

class BackendBase(metaclass=ABCMeta):
    '''Base for the backend'''
    _running = threading.Event()
    _event_lock = threading.Event()
    _event_list = []
    _event_list_lock = threading.Lock()

    __thread_run = True

    _conn = None

    def __init__(self):
        '''INIT'''
        self.__thread = threading.Thread(target=self.run, args=())
        self.__thread.setName("DATABASE")
        self.__thread.start()
        self._running.wait()

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
            self._event_lock.set()
            self.__thread.join()

    @property
    def thread_run(self) -> bool:
        '''return if thread is running'''
        return self.__thread.is_alive()


##################
##USER FUNCTIONS##
##################
    def call(self, message: SQLMessage):
        '''function to pass the query/table through to the backend thread'''
        if not isinstance(message, SQLMessage):
            return None
        with self._event_list_lock:
            self._event_list.append(message)
        self._event_lock.set()
        message.event_wait()

##########
##THREAD##
##########
    def run(self):
        '''Threadded Run'''
        self._startup()
        self._running.set()
        while self.__thread_run:
            self.__run_loop()
        self._shutdown()

    def __run_loop(self):
        '''run commands'''
        self._event_lock.wait()
        while self._event_list:
            with self._event_list_lock:
                job = self._event_list.pop()
            if isinstance(job, SQLMessage):
                self.__run_message_action(job)
            else:
                print("WTF IS PASSED IN???", type(job), job)
        self._event_lock.clear()

    def __run_message_action(self, job: SQLMessage):
        if isinstance(job.query, Table):
            if self._table_check(job.query):
                job.event_set()
            else:
                raise TableCheckFailure
        else:
            self.__do_job(job)

    def __do_job(self, job: SQLMessage):
        '''do the magic work for each job'''
        cursor = self._get_cursor()
        cursor.execute(job.query)
        BackendBase._conn.commit()
        data = cursor.fetchall()
        if len(data) == 1:
            job.return_data = data.pop()
            job.event_set()
            return
        job.return_data = data
        job.event_set()

    @abstractmethod
    def _startup(self):
        '''Setup the System Here'''

    @abstractmethod
    def _shutdown(self):
        '''Shutdown the System Here'''

    @abstractmethod
    def _get_cursor(self):
        '''returns a sql cursor'''

    @abstractmethod
    def _table_check(self, table: Table) -> bool:
        '''Check, Create or Update Table in DB.'''
