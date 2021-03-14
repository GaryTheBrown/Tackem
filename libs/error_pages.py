'''Error Pages'''
import cherrypy


def setup_error_pages(
        e400: bool = True,
        e401: bool = True,
        e403: bool = True,
        e404: bool = True,
        e500: bool = True
):
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

# def error_page_400(status, message, traceback, version) -> str:


def error_page_400(status, message, traceback, version) -> str:
    '''400 error page'''
    return 'Error 400 Bad Request'


def error_page_401(status, message, traceback, version) -> str:
    '''401 error page'''
    return 'Error 401 Unauthorized'


def error_page_403(status, message, traceback, version) -> str:
    '''403 error page'''
    return 'Error 403 Forbidden'


def error_page_404(status, message, traceback, version) -> str:
    '''404 error page'''
    return 'Error 404 Page not found'


def error_page_500(status, message, traceback, version) -> str:
    '''500 error page'''
    return 'Error:500 Internal Server Error'
