{
    'name': 'Приём в магистратуру',
    'summary': 'Software to admission masters at HSE',
    'author': 'Vadim Zakharov',
    'category': 'Extra Tools',
    'version': '1.0',
    'license': 'AGPL-3',
    # модули необходимые для работы приложения
    'depends': [
        'base',
        'board',
        'mail',
        'website',
        'website_slides'
    ],
    # загружается при запуске
    'data': [
        #'security/security.xml',
        'security/ir.model.access.csv',
        'views/main.xml',
        'views/form.xml',
        'views/employee.xml',
        'views/event.xml',
        'views/point.xml',
        'data/mail_template.xml',
        #'data/notification_template.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
