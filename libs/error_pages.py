'''Error Pages'''
import cherrypy


def setup_error_pages(e400=True, e401=True, e403=True, e404=True, e500=True):
    '''Changes the Error Pages For The System'''
    if e400:
        cherrypy.config.update({'error_page.400': error_page_400})

    if e401:
        cherrypy.config.update({'error_page.401': error_page_401})

    if e403:
        cherrypy.config.update({'error_page.403': error_page_403})

    if e404:
        cherrypy.config.update({'error_page.404': error_page_404})

    if e500:
        cherrypy.config.update({'error_page.500': error_page_500})


def error_page_400(status, message, traceback, version):
    '''400 error page'''
    return ('Error 400 Bad Request')


def error_page_401(status, message, traceback, version):
    '''401 error page'''
    return ('Error 401 Unauthorized')


def error_page_403(status, message, traceback, version):
    '''403 error page'''
    return ('Error 403 Forbidden')


def error_page_404(status, message, traceback, version):
    '''404 error page'''
    return ('Error 404 Page not found')


def error_page_500(status, message, traceback, version):
    '''500 error page'''
    return ('Error:500 Internal Server Error')
