# -*- coding:utf-8 -*-
# @module RequestsStorage
# @desc Storage for requests records
# @since 2022.03.25, 19:19
# @changed 2022.04.03, 21:46

# Mail server usage
# (from https://habr.com/ru/post/348566/)
#
# (1) Use fake mail server: `python -m smtpd -n -c DebuggingServer localhost:8025`
# MAIL_SERVER=localhost
# MAIL_PORT=8025
#
# (2) Use real smtp server with env params:
# MAIL_SERVER=smtp.googlemail.com
# MAIL_PORT=587
# MAIL_USE_TLS=1
# MAIL_USERNAME=<your-gmail-username>
# MAIL_PASSWORD=<your-gmail-password>


import traceback
#  from os import path

from flask_mail import Mail, Message

from config import config

from src.app import app

from src.core.lib.logger import DEBUG
from src.core.lib.utils import getTrace

from src.core.Requests import RequestsConstants


# @see https://flask.palletsprojects.com/en/2.0.x/config/#configuration-basics
app.config.update(
    #  MAIL_SERVER='smtp.googlemail.com',  # gmail
    MAIL_SERVER='smtp.fullspace.ru',  # @see https://client.fullspace.ru/virt/mail/?domain=march.team
    MAIL_PORT=25,
    MAIL_USE_TLS=0,
    #  MAIL_PORT=465,
    #  MAIL_USE_TLS=1,
    #  MAIL_USERNAME='lilliputten@gmail.com',
    #  MAIL_USERNAME='march.team.realty@gmail.com',
    MAIL_USERNAME=config['mailUser'],
    MAIL_PASSWORD=config['mailPass'],
    TESTING=config['isTest'],
    #  SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)


mailer = Mail(app)


def getRecordParamsHtmlText(data):
    keys = RequestsConstants.translateKeys.keys()
    params = []
    for key in keys:
        if key in data and data[key]:
            name = RequestsConstants.translateKeys[key]
            val = data[key]
            params.append(f"<p class=\"Param\"><span class=\"Label\">{name}:</span> {val}</p>")
    return "\n        ".join(params)


def getRecordParamsPlainText(data):
    keys = RequestsConstants.translateKeys.keys()
    params = []
    for key in keys:
        if key in data and data[key]:
            name = RequestsConstants.translateKeys[key]
            val = data[key]
            params.append(f"{name}: {val};")
    return "\n".join(params)


def getRecordMailSubject(data):
    requestType = data['requestType']
    subject = requestType
    if requestType in RequestsConstants.requestTypeNames:
        subject = RequestsConstants.requestTypeNames[requestType] + ' (' + requestType + ')'
    return subject


def createRecordMailHtmlMsg(data):
    title = getRecordMailSubject(data)
    paramsStr = getRecordParamsHtmlText(data)
    # TODO: Add favicon links into html message head section? How?
    html = f"""
    <link rel="icon" type="image/svg" href="https://march.team/static/herb-on-dark/simple/logo-simple-herb-with-bg.svg" />
    <link rel="icon" type="image/png" href="https://march.team/static/herb-on-dark/simple/logo-simple-herb-with-bg-256.png" />
    <style><!--
    {RequestsConstants.mailMsgStyles}
    --></style>
    <h2 class="Title">{title}</h2>
    <div class="Params">
        {paramsStr}
    </div>
    <div class="Footer">
        Компания «Март-Недвижимость»<br/>
        Web: <a href="https://march.team">https://march.team</a><br/>
        E-mail: <a href="mailto:mail@march.team">mail@march.team</a><br/>
        Телефон: <a href="tel:+79957907010">+7 (995) 790 70 10</a><br/>
    </div>
    """
    DEBUG(getTrace(), {
        #  'data': data,
        #  'paramsStr': paramsStr,
        'html': html,
    })
    return html


def createRecordMailPreviewText(data):
    return getRecordParamsPlainText(data)


def sendRecordMail(data):
    try:
        subject = getRecordMailSubject(data)
        html = createRecordMailHtmlMsg(data)
        textPreview = createRecordMailPreviewText(data)
        isDev = config['isDev']
        sender = config['mailFromAddr']
        recipients = config['mailToBCCAddr'] if isDev else config['mailToAddr']
        bcc = None if isDev else config['mailToBCCAddr']
        msg = Message(
            subject,
            sender=sender,
            recipients=recipients,
            bcc=bcc,
            body=textPreview,
        )
        msg.html = html
        isDev = config['isDev']
        DEBUG(getTrace(), {
            'isDev': isDev,
            'data': data,
            'html': html,
            'textPreview': textPreview,
            'msg': msg,
            'sender': sender,
            'recipients': recipients,
            'bcc': bcc,
        })
        # Send mail if not dev-server
        #  if not isDev:
        mailer.send(msg)
    except Exception as err:
        sTraceback = str(traceback.format_exc())
        DEBUG(getTrace('catched error'), {
            'err': err,
            'traceback': sTraceback,
        })
        #  #  errStr = 'Cannot execute db command: ' + dbCmd
        #  raise Exception(errStr) from err
        raise err


__all__ = [  # Exporting objects...
    'createRecordMailHtmlMsg',
]


if __name__ == '__main__':
    DEBUG(getTrace(' debug run'))
