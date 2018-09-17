'''API FOR PLUGIN'''
import cherrypy
class Root():
    '''ROOT OF PLUGINS WEBUI HERE'''

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        '''GET'''
        return 'GET'

    def POST(self):
        '''POST'''
        return 'POST'

    def PUT(self):
        '''PUT'''
        return 'PUT'

    def DELETE(self):
        '''DELETE'''
        return 'DELETE'
