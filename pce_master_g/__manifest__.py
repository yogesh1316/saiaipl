{
    'name': 'PCE Master',
    'version': '11.0.1.0.0',
    'summary': 'PCE Master',
    'author': 'Pradip',
    'website': 'www.saiaipl.com',
    'license': 'AGPL-3',
     'depends': [
         'sale','product','sale_margin','purchase','crm','account','base',
     ],
    'data': [
        'views/pce_master_menu_views.xml',
        'views/reason_master_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
