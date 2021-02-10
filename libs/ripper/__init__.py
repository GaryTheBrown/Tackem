'''Ripper init'''
from data.config import CONFIG

# TODO Pull Ripper plugin back into the System with checks for programs to load system then checks
# on if drives exist and give the option of ripping locally or just giving ISO
# TODO Allow ripper to just accept ISOs instead if no drives in the machine.
# then we can create some api call to say there is a new ISO to work with,
# would need to check the process of getting info from the bluray for it's codes we are using.
# a seperate system for ripping drives should be created as another app.
# https://askubuntu.com/questions/147800/ripping-dvd-to-iso-accurately

#new way needs user to set the amount of makemkv instances allowed and if drives lock one each
#one thread does the watching and starts up the relevent tasks in another thread.
class Ripper:
    '''Main Class to create an instance of the plugin'''

    def __init__(self):
        '''setup systems'''
        if CONFIG['ripper']['enabled'].value is False:
            return

        self._drives = []
        self._video_labeler = None
        self._converter = None
        self._renamer = None
        self._running = False

        if CONFIG['ripper']['drives']['enabled'].value:






            self.__setup_drives()
        elif CONFIG['ripper']['iso']['enabled'].value:
            self.__setup_iso()

    def __setup_drives(self):
        '''Setup the Drives'''

    def __setup_iso(self):
        '''Setup the iso'''





        Database.call(SQLTable(db_tables.VIDEO_INFO_DB_INFO))
        Database.call(SQLTable(db_tables.VIDEO_CONVERT_DB_INFO))

        for location in ROOT_Config['ripper']['locations']:
            folder = ROOT_Config['ripper']['locations'][location].value
