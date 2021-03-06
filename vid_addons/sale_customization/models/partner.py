from openerp import models, fields, api, _


class CustomerType(models.Model):
    _name = 'customer.type'
    _rec_name = 'customer_type'

    customer_type = fields.Char(string='Customer Type')
    
class ResPartner(models.Model):
    _inherit = 'res.partner'

    disc = fields.Float(string='Normal Discount %')
    adisc = fields.Float(string='Additional Discount')
    tdisc = fields.Float(string='T Discount %')
    nedisc = fields.Float(string='Non-Excise Discount %')
    customer_type = fields.Many2one('customer.type', string='Customer Type')
    lead_time = fields.Integer("Lead Time")
    tax_id = fields.Many2many("account.tax", "form_wise_tax_in_partner", "partner_id", "taxes_id", "Customer Taxes")
    tax_desc = fields.Text("Tax Description")
    # partner_selling_type = fields.Selection([('normal', 'Normal'), ('special', 'Special'),('extra', 'Extra')],string='Partner Selling Type')
    # partner_selling_type_id = fields.Many2one('partner.selling.type',string='Partner Selling Type-Discount')
    
    # def name_get(self, cr, uid, ids, context=None):
    #     res = []
    #     for inst in self.browse(cr, uid, ids, context=context):
    #         name = inst.name or '/'
    #         if name and inst.zip:
    #             name = name+' ,'+inst.zip
    #         if name and inst.city:
    #             name = name+' ,'+inst.city
    #         if name and inst.street:
    #             name = name+' ,'+inst.street
    #         res.append((inst.id, name))
    #     return res






