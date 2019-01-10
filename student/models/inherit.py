from odoo import models, fields, api
class sale_order_inhe(models.Model):
    _inherit ='sale.order'
    name=fields.Char(string="firstname")
    last_name=fields.Char(string="last name")