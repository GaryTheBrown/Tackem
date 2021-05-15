"""
Creates checksum hash for a file in Binary from SHA256
If storing in the DB you need a BINARY(32)
"""
import threading

from database.library.file import LibraryFile


class FileChecker:
    """system to check the files are not damaged"""

    __event = threading.Event()
    __thread = None
    __thread_run = False
    __active = False

    @classmethod
    def start(cls):
        """starts the file checker"""
        cls.__thread = threading.Thread(target=cls.__run, args=())
        cls.__thread.setName("Library File Checker")
        if cls.__thread_run is False:
            cls.__thread_run = True
            cls.__thread.start()

    @classmethod
    def stop(cls):
        """stops the Library"""
        if cls.__thread_run is True:
            cls.__thread_run = False
            cls.__event.set()

    @classmethod
    def run(cls) -> bool:
        """set the File checker to run"""
        if cls.__active is False:
            cls.__event.set()
            return True
        return False

    @classmethod
    def __run(cls):
        """Threadded Script For running"""
        while cls.__thread_run:
            cls.__event.wait()
            cls.__active = True
            if not cls.__thread_run:
                return

            files = LibraryFile.files_to_check()
            while file := files.pop():
                if not cls.__thread_run:
                    return
                file.check_file()

            cls.__active = False
            cls.__event.clear()
            if not cls.__thread_run:
                return
