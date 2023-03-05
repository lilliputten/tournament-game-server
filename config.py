# -*- coding:utf-8 -*-
# @module config
# @desc Universal server & client config
# @since 2022.02.06, 23:56
# @changed 2023.03.06, 00:59
# See:
#  - https://docs.python.org/3/library/configparser.html -- ???
#  - https://stackoverflow.com/questions/9590382/forcing-python-json-module-to-work-with-ascii
#  - https://flask.palletsprojects.com/en/2.0.x/config/

import os
from os import path
import json
#  import yaml
import sys

from config_helpers import updateConfigWithYaml, readFiletoString

pythonVersion = sys.version

#  Determine running under test suite...
isTest = 'unittest' in sys.modules

gunicornEnv = os.getenv('GUNICORN_ENV')  # Detect gunicorn server (run on a raspberry pi)
flaskEnv = os.getenv('FLASK_ENV')  # detect flask server (dev mode)
isGunicorn = bool(gunicornEnv)
isRPi = isGunicorn
isDev = flaskEnv == 'development' or isTest
isProd = not isDev
# TODO: Detect test environment

rootPath = path.dirname(path.abspath(__file__))  # Project root path

yamlConfigFilename = path.join(rootPath, 'config.yml')
yamlLocalConfigFilename = path.join(rootPath, 'config.local.yml')

uploadPath = path.join(rootPath, 'uploads')

# Project structure

# (UNUSED) See link creation in `utils/make-html-app-links.sh`, `utils/make-html-app-links-local.sh`
#  Generate/read build parameters (version, timetag etc)
#  Default values (empty)...
version = ''
timestamp = ''
timetag = ''
buildTag = ''
#  Filenames...
buildVersionFilename = path.join(rootPath, 'build-version.txt')
buildTagFilename = path.join(rootPath, 'build-tag.txt')
timestampFilename = path.join(rootPath, 'build-timestamp.txt')
timetagFilename = path.join(rootPath, 'build-timetag.txt')
packageFilename = path.join(rootPath, 'package.json')
#  Read version...
#  print('config: packageFilename', packageFilename)  # DEBUG
if path.isfile(buildVersionFilename):
    version = readFiletoString(buildVersionFilename, 'UNSPECIFIED')
elif path.isfile(packageFilename):
    with open(packageFilename, encoding='utf-8') as pkgConfigFile:
        pkgConfig = json.load(pkgConfigFile)
        version = pkgConfig['version'].encode('ascii')
        #  pkgConfigFile.close()
# Read timestamp/timetag...
if path.isfile(timestampFilename):
    timestamp = readFiletoString(timestampFilename)
if path.isfile(timetagFilename):
    timetag = readFiletoString(timetagFilename)
# Read/generate buildTag...
if version and timetag:
    buildTag = 'v.' + version + '-' + timetag
elif path.isfile(buildTagFilename):
    buildTag = readFiletoString(buildTagFilename)

config = {  # Default config

    # Application parameters...

    'flaskEnv': flaskEnv,
    'gunicornEnv': gunicornEnv,
    'isGunicorn': isGunicorn,
    'isRPi': isRPi,
    'isDev': isDev,
    'isProd': isProd,
    'isTest': isTest,

    'pythonVersion': pythonVersion,
    'version': version,
    'timestamp': timestamp,
    'timetag': timetag,
    'buildTag': buildTag,

    'errorSendCode': True,
    'errorResponseType': 'text',
    #  'errorResponseType': 'json',

    # Path parameters...

    'rootPath': rootPath,  # RO!
    'uploadPath': uploadPath,

    # Generated client path (see `cam-client-app-build`, TODO?)

    #  'clientTemplatePath': path.join(rootPath, 'cam-client-app-build'),
    'clientTemplatePath': path.join(rootPath, 'src/templates'),
    'clientStaticPath': path.join(rootPath, 'static'),
    #  'clientStaticPath': path.join(clientTemplatePath, 'static'),
    'clientStaticUrl': '/static',
    #  'clientStaticUrl': '',

    # Logging...

    'outputLog': True,  # Print log to stdout
    'outputColoredLog': True,  # Use rich output log format with `termcolor`
    'writeLog': True,  # Write log to external file
    'clearLogFile': True,  # Clear log file at start
    'logFileName': 'log.txt',  # Log file name (relative to `rootPath`!)

    # Datetime formats...

    'dateTagFormat': '%y%m%d-%H%M',  # eg: '220208-0204'
    'dateTagPreciseFormat': '%y%m%d-%H%M%S',  # eg: '220208-020423'
    'shortDateFormat': '%Y.%m.%d %H:%M',  # eg: '2022.02.08-02:04'
    'preciseDateFormat': '%Y.%m.%d %H:%M:%S',  # eg: '2022.02.08-02:04:23'
    'logDateFormat': '%y%m%d-%H%M%S-%f',  # eg: '220208-020423-255157'
    'detailedDateFormat': '%Y.%m.%d %H:%M:%S.%f',  # eg: '2022.02.08-02:04:23.255157'

    # Databases...

    'dbPath': path.join(rootPath, 'db'),
    #  'dbExt': '.db',  # sqlite3 database file extensions
    'dbExt': '.json',  # tinydb database file extensions

    # Questions...

    'questionsCount': 2 if isDev else 5,  # Questions number for each quiz session (selecting randomly -- see parameter `useRandomQuestions` -- in `Questions:getClientQuestionIdsList`)
    'useRandomQuestions': False if isDev else True,  # To creatre questions list random
    'validQuestionsPeriodMs': 15 * 60 * 1000,  # X mins, Time to update questions list from disk file, see `Questions:getOrLoadQuestionsData`.
    'recordsTableSize': 15 if isDev else 20,  # Size of game records table

    # API

    'legalOrigins': [
        # Real endpoint addresses...
        'https://tournament-game-build.march.team',
        'http://tournament-game-build.march.team',
    ],

    'apiRoot': '/api/v1.0',  # Eg: http://localhost:5000/api/v1.0/start
    'apiUser': 'api',
    'apiPass': 'pusplndvqaivbynv',  # Authorization: Basic YXBpOnB1c3BsbmR2cWFpdmJ5bnY=

    # Send mail

    'mailFromAddr': '"Tournament Site" <tournament@march.team>',
    'mailToAddr': ['tournament@march.team'],
    'mailToBCCAddr': ['dmia@yandex.ru'],

    'mailUser': 'site@march.team',
    'mailPass': 'M1qcqujpwflapqfgh',  # App pwd for `site@march.team`
    #  'mailUser': 'march.team.realty@gmail.com',
    #  'mailPass': 'mqcqujpwflapqfgh',  # App pwd for `march.team.realty@gmail.com`

}

# Allows CORS requests from developer (localhost) server (NOTE: allow it only on developing cycle)
allowDebugOrigins = True
if allowDebugOrigins:
    config['legalOrigins'].append('http://localhost:3000')
    config['legalOrigins'].append('http://localhost:5000')


updateConfigWithYaml(config, yamlConfigFilename)
updateConfigWithYaml(config, yamlLocalConfigFilename)


__all__ = [  # Exporting objects...
    'config',
]


if __name__ == '__main__':
    print('@:config: debug run')
