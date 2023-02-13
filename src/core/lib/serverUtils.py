# -*- coding:utf-8 -*-
# @module serverUtils
# @desc Helper soutines for server.
# @since 2022.02.12, 02:41
# @changed 2023.02.13, 23:26

import traceback

from flask import redirect
from flask import request
from flask import session
from flask import jsonify
#  from flask import render_template
#  from flask import request
#  from config import config

from config import config
from src import appSession

from src.core.lib.logger import DEBUG
from src.core.lib import errors
from src.core.lib.utils import getTrace


def makeErrorResponse(errorData):
    # @see https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    code = errorData['code'] if 'code' in errorData else 500
    DEBUG(getTrace(), {
        #  'keys': list(keys),
        'code': code,
        'errorData': errorData,
    })
    # NOTE: Don't send http error codes so it breaks down CORS requests!
    resCode = code if config['errorSendCode'] else 200
    if config['errorResponseType'] == 'json':  # json
        return jsonify(errorData), resCode
    keys = errorData.keys()
    result = ''
    for key in keys:
        val = errorData[key]
        result += key + ': ' + str(val) + '\n'
    return result, resCode, {
        'Content-Type': 'text/plain; charset=utf-8',
    }
    #  return render_template('error-not-found.html', error=error), code


def makeErrorForRequest(errDict):
    if errDict is None:
        errDict = {}
    error = errDict.get('error', 'Endpoint not found')
    code = errDict.get('code', 404)
    url = errDict.get('url', request.url)
    method = errDict.get('method', request.method)
    protocol = errDict.get('protocol', request.scheme)
    reason = errDict.get('reason', '')  # Only for dev mode?
    errorData = {
        'error': error,
        'code': code,
        #  'systemError': error,
        'url': url,
        'method': method,
        'protocol': protocol,
        'reason': reason,
        #  'repr': errorRepr,
    }
    DEBUG(getTrace(), {
        'errDict': errDict,
        'errorData': errorData,
    })
    return makeErrorResponse(errorData)


def getEnvironData():
    environ = request.environ
    data = {}
    keys = environ.keys()
    for key in keys:
        val = str(environ[key])
        data[key] = val
    return data


def getOrigin():
    #  environData = getEnvironData()
    environ = request.environ
    return environ.get('HTTP_ORIGIN')


def getRequestData():
    environData = getEnvironData()
    origin = environData.get('HTTP_ORIGIN')
    ip = request.remote_addr
    url = request.url
    method = request.method
    protocol = request.scheme
    tokenSession = session.get('Token')
    cookies = request.cookies
    tokenCookie = cookies.get('Token')
    requestData = {
        'origin': origin,
        'ip': ip,
        'url': url,
        'method': method,
        'protocol': protocol,
        'tokenSession': tokenSession,
        'tokenCookie': tokenCookie,
        #  'cookies': cookies,
        'environment': environData,
    }
    return requestData


def getBadRequestResponse(reason):
    requestData = getRequestData()
    errorData = {
        'code': 400,
        'error': 'Bad Request',
        'reason': reason,
    }
    DEBUG(getTrace(reason), dict(requestData, **{'errorData': errorData}))
    return makeErrorForRequest(errorData)


def checkInvalidRequestError(checkToken=True, checkGameToken=False, checkRequestJsonData=False):
    # Prepare parameters...
    origin = getOrigin()
    # If invalid origin then return error...
    legalOrigins = config['legalOrigins']
    if origin is None or origin not in legalOrigins:
        return getBadRequestResponse('Invalid request origin')
    if checkToken and not appSession.hasValidToken():
        return getBadRequestResponse('Invalid token')
    if checkGameToken and not appSession.hasValidGameToken():
        return getBadRequestResponse('Invalid gameToken')
    if checkRequestJsonData:
        requestData = request.json  # request.values
        if requestData is None or not requestData:
            return getBadRequestResponse('Invalid request data')
    return None  # Success: No error -- we can to process this request further


def server_handle_not_found(err):
    # TODO: Determine not found page url
    error = errors.toString(err)
    #  errorRepr = err.__repr__()
    code = getattr(err, 'code', 404)
    url = request.url
    method = request.method
    protocol = request.scheme
    errorData = {
        'code': code,
        'error': 'Resource not found',
        #  'systemError': error,
        'url': url,
        'method': method,
        'protocol': protocol,
        #  'repr': errorRepr,
    }
    DEBUG(getTrace(), dict(errorData, **{'systemError': error}))
    return makeErrorResponse(errorData)


def server_handle_exception(err):
    #  errorType, errorValue, errorTraceback = sys.exc_info()
    #  @see https://docs.python.org/2/library/traceback.html
    #  code = err.code if hasattr(err, 'code') else None  # http response code (if http error)
    code = getattr(err, 'code', 500)
    if code:  # Skip non-errors...
        if code == 308 and err.new_url:  # Skip redirect errors...
            new_url = err.new_url
            DEBUG(getTrace('redirect'), {
                'code': code,
                'new_url': new_url,
                'error': err,
            })
            return redirect(new_url)
        # TODO: Other non-errors?
        #  if code >= 200 and code < 400:
    errorTraceback = traceback.format_exc()
    tracebackStr = str(errorTraceback)
    error = errors.toString(err)
    url = request.url
    method = request.method
    protocol = request.scheme
    #  errorRepr = err.__repr__()
    errorData = {
        'code': code,
        'error': error,
        'url': url,
        'method': method,
        'protocol': protocol,
        #  '_note': 'See detailed info & traceback in server logs.',
        #  'repr': errorRepr,
        #  'traceback': tracebackStr,
    }
    if config['isDev']:
        errorData['traceback'] = tracebackStr
    else:
        errorData['error'] += ' (See detailed info & traceback in server logs)'
    DEBUG(getTrace(), dict(errorData, **{'traceback': tracebackStr}))
    return makeErrorResponse(errorData)


if __name__ == '__main__':
    DEBUG(getTrace('debug run'))
