# -*- coding:utf-8 -*-
# @module blueprintTest
# @desc Test camera shot api
# @since 2022.02.12, 01:46
# @changed 2022.02.12, 01:46

#  from flask import Blueprint
#  from flask import render_template
#  from flask import session
from flask import Blueprint
#  from flask import redirect
#  from flask import render_template
#  from flask import url_for
#  from flask import jsonify
#  from flask import request

#  from config import config

from src.core.lib.logger import DEBUG
#  from .app import app

#  from flask import session

#  session.init_app(app)

blueprintTest = Blueprint('blueprintTest', __name__)

#  # NOTE: Logged twice with `* Restarting with stat` in dev mode
#  DEBUG('@:blueprintTest: starting', {
#      'buildTag': config['buildTag'],
#  })


# Tests...


sharedVars = {
    'name': None,
}


#  @blueprintTest.route('/')
#  @blueprintTest.route('/<name>')  # May conflict with static resources like `/favicon.ico`
#  def route_root(name=None):
#      #  return '<p>Hello, World!</p>'
#      fromId = '@:blueprintTest:route_root'
#      data = {
#          'fromId': fromId,
#          'name': name,
#      }
#      DEBUG(fromId, data)
#      #  return 'blueprintTest:route_root: ' + session.get('name', '')
#      return render_template('hello.html', name=name)


@blueprintTest.route('/user/<name>')
def route_user(name):
    #  return 'blueprintTest: Raw html: User: %s' % name
    return f'blueprintTest: Raw html: User: {name}'
    #  res = jsonify(data)
    #  return res


__all__ = [  # Exporting objects...
    'blueprintTest',
]

if __name__ == '__main__':
    DEBUG('@:blueprintTest: debug run')
