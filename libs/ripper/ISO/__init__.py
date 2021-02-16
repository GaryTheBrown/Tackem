'''Root system for ISO Ripping using a Folder watcher'''
from threading import BoundedSemaphore
from watchdog.events import FileSystemEvent, PatternMatchingEventHandler
from watchdog.observers import Observer

from data.config import CONFIG

class ISO:
    '''Root system for ISO Ripping using a Folder watcher'''

    __pool_sema = None
    __audio_watcher = None
    __video_watcher = None
    __audio_observer = None
    __video_observer = None

    @classmethod
    def start(cls):
        '''Starts the ripper ISO Watcher'''
        cls.__pool_sema = BoundedSemaphore(value=CONFIG['ripper']['iso']['threadcount'].value)

    @classmethod
    def watcher_setup(cls):
        '''Sections for setting up the folder watcher watchdog'''
        patterns = "*"
        ignore_patterns = ""
        ignore_directories = False
        case_sensitive = True
        cls.__audio_watcher = PatternMatchingEventHandler(
            patterns,
            ignore_patterns,
            ignore_directories,
            case_sensitive)

        cls.__video_watcher = PatternMatchingEventHandler(
            patterns,
            ignore_patterns,
            ignore_directories,
            case_sensitive)

        cls.__audio_watcher.on_created = cls.__audio_file_detected
        cls.__audio_watcher.on_modified = cls.__audio_file_detected
        cls.__video_watcher.on_created = cls.__video_file_detected
        cls.__video_watcher.on_modified = cls.__video_file_detected

        audio_path = CONFIG['ripper']["locations"]["videoiso"].value
        video_path = CONFIG['ripper']["locations"]["audioiso"].value

        cls.__audio_observer = Observer()
        cls.__audio_observer.schedule(cls.__audio_watcher, audio_path, recursive=True)

        cls.__video_observer = Observer()
        cls.__video_observer.schedule(cls.__video_watcher, video_path, recursive=True)

    @classmethod
    def __audio_file_detected(cls, event: FileSystemEvent):
        '''action when a new audio ISO is detected'''
        with cls.__pool_sema:
            #TODO
            pass

    @classmethod
    def __video_file_detected(cls, event: FileSystemEvent):
        '''action when a new video ISO is detected'''
        with cls.__pool_sema:
            #TODO
            pass
