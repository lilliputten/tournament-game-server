# -*- coding:utf-8 -*-
# @module RequestsConstants
# @desc Requests Constants
# @since 2022.03.25, 22:20
# @changed 2022.04.03, 21:43


dbName = 'RequestsStorage'  # Relative to `config['dbPath']`

requestTypeNames = {
    'Test': 'Тестовый запрос',
    'RequestDetails': 'Запрос подробной информации',
    'BuyApartmentRequest': 'Заявка на покупку объекта недвижимости',
    'Consultations': 'Заявка на консультацию',
    'BuyApartment': 'Заявка на покупку квартиры',
    'SellApartment': 'Заявка на продажу квартиры',
    'OrderCallback': 'Заявка на обратный звонок',
}

translateKeys = {
    'SlideId': 'Слайд',
    'FromPage': 'Со страницы',
    'Name': 'Имя',
    'FirstName': 'Имя',
    'LastName': 'Фамилия',
    'PhoneNumber': 'Телефон',
    'EMail': 'E-mail',
    'ApartmentType': 'Тип квартиры',
    'Location': 'Расположение',
    'ConvenientTime': 'Удобное для звонка время',
    'ip': 'IP адрес',
    'Token': 'Сессия',
    'timestr': 'Запись создана',
}

mailMsgStyles = """
    .Title {
        font-weight: normal;
    }
    .Label {
        color: gray;
        opacity: .5;
    }
    .Params {
        margin: 2em 0;
    }
    .Footer {
        color: gray;
        line-height: 1.8;
        letter-spacing: 2px;
        opacity: .5;
        font-size: small;
        font-style: italic;
        border-top: 1px solid gray;
        margin-top: 3em;
        padding-top: 1em;
    }
"""

__all__ = [  # Exporting objects...
    'dbName',
    'requestTypeNames',
    'translateKeys',
    'mailMsgStyles',
]
