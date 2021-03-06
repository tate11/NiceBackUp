# -*- coding: utf-8 -*-
{
    'name': "Dispatch Document",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "VIDTS",
    'website': "http://www.vidts.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Dispatch',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        
        'report.xml',
        'views/lr_doc_view.xml',
        'views/report_lr_doc.xml',
        'views/account_invoice_view.xml',
        'views/print_on_envolope.xml',
        'views/port_code_views.xml',
        'data/lr_data.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],

    'application':True
}