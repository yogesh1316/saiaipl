
from odoo import fields,api,models
from odoo.exceptions import UserError

class inheritance_view_file(models.Model):
    _inherit="sale.order"
    tax_line_id=fields.Many2many('account.tax', string='Taxes',domain=['|', ('active', '=', False), ('active', '=', True)])
    tax_group_chkbox=fields.Boolean('Set Taxes For Order Line',compute='checkbox_checked_unchecked',store=True,readonly=False)
    revise_order_checkbox=fields.Boolean('Revise The Qutation')
    sale_line=fields.One2many("sale.order.revise",'sale_id')
    revise_count=fields.Integer("Revise Count")
    revise_name=fields.Char("name",readonly=True, store=True)
    
    @api.multi
    def write(self,vals):
        print("vals",vals)
        if "revise_order_checkbox" in vals:
            if vals["revise_order_checkbox"]==True:  
                print("I m in .........")
            self.create_revision()
            self.revise_count=self.revise_count + 1
            self.revise_name="REV-" + (str(self.revise_count))
            vals["revise_order_checkbox"]=False
        variable=super(inheritance_view_file,self).write(vals)
        return variable

    @api.multi
    def create_revision(self):
        revision_vals={
            'revise_name':self.revise_name,
            'sale_id':self.id,
            'name':self.name,
            'partner_id':self.partner_id.id,
            'validity_date':self.validity_date,
            'payment_term_id':self.payment_term_id.id,
            'user_id':self.user_id and self.user_id.id,
            'client_order_ref':self.client_order_ref,
            'team_id':self.team_id.id,
            'date_order':self.date_order,
            'fiscal_position_id':self.fiscal_position_id.id,
            'origin':self.origin,
            # 'margin':self.margin,
            'partner_invoice_id':self.partner_invoice_id.id,
            'partner_shipping_id':self.partner_shipping_id.id,
            'pricelist_id':self.pricelist_id.id,
            'amount_untaxed':self.amount_untaxed, 
            'amount_tax':self.amount_tax,
            'amount_total':self.amount_total
            }            
        sale_order_revise_obj=self.env['sale.order.revise'].create(revision_vals)
        sale_order_revise_obj.sale_id=self.id
        categ_id=0
        for i in self.order_line: 
            if i.layout_category_id.id:
                 categ_id=i.layout_category_id.id
            line_rivision_vals={
                'sale_orderrevise_id':sale_order_revise_obj.id,
                'layout_category_id':categ_id,
                'discount':i.discount,
                'product_id':i.product_id.id,
                'name':i.name,
                'product_uom_qty':i.product_uom_qty,
                'price_unit':i.price_unit,
                'tax_id':i.tax_id,
                'price_subtotal':i.price_subtotal,
                'order_id':self.id,
                'product_uom':i.product_uom,
                # 'purchase_price':i.purchase_price     
            }
            sale_order_revise_obj.sale_orderlinerevise_line=[(0,0,line_rivision_vals)]
            sale_order_revise_obj.sale_id=self.id
                
    @api.depends('order_line.tax_id')
    def checkbox_checked_unchecked(self):
        for order in self: 
            if order.order_line:
                print("1234")
                for line in order.order_line:
                    if order.tax_line_id != line.tax_id:
                        print("56789")
                        order.tax_group_chkbox = False
                    else:
                        order.tax_group_chkbox = True


    @api.onchange('tax_line_id')
    def default_tax_id_for_child(self):
        for order in self:
            for line in order.order_line:
                line.tax_id=order.tax_line_id
   

class SaleOrderRevise(models.Model):
    _name="sale.order.revise"
    revise_name=fields.Char("Sale Order Revise Count", readonly=True, store=True)
    sale_id=fields.Many2one("sale.order")
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    sale_orderlinerevise_line=fields.One2many("sale.order.line.revise",'sale_orderrevise_id')
    # margin = fields.Monetary(help="It gives profitability by calculating the difference between the Unit Price and the cost.",store=True)
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self:('New'))
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True, change_default=True, index=True, track_visibility='always')
    validity_date = fields.Date(string='Expiration Date', readonly=True, copy=False, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},help="Manually set the expiration date of your quotation (offer), or it will set the date automatically based on the template if online quotation is installed.",store=True)
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term',store=True)
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', default=lambda self: self.env.user)
    client_order_ref = fields.Char(string='Customer Reference', copy=False)
    team_id = fields.Many2one('crm.team', 'Sales Channel', change_default=True, oldname='section_id')
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now)
    fiscal_position_id = fields.Many2one('account.fiscal.position', oldname='fiscal_position',string='Fiscal Position')
    origin = fields.Char(string='Source Document', help="Reference of the document that generated this sales order request.")
    partner_invoice_id = fields.Many2one('res.partner', string='Invoice Address', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Invoice address for current sales order.",store=True)
    partner_shipping_id = fields.Many2one('res.partner', string='Delivery Address', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Delivery address for current sales order.",store=True)
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Pricelist for current sales order.")
    currency_id = fields.Many2one("res.currency", related='pricelist_id.currency_id', string="Currency", readonly=True, required=True)
    amount_untaxed = fields.Monetary('Untaxed Amount', store=True)
    amount_tax = fields.Monetary('Taxes',store=True)
    amount_total = fields.Monetary('Total',store=True)


class SaleOrderLine(models.Model):
    _inherit="sale.order.line"


class SaleOrderLineRevise(models.Model):
    _name="sale.order.line.revise"
    sale_orderrevise_id=fields.Many2one("sale.order.revise")
    layout_category_id = fields.Many2one('sale.layout_category', string='Section',store=True)
    discount = fields.Float(string='Discount (%)',default=0.0,store=True)
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', required=True,store=True)
    name = fields.Text(string='Description', required=True,store=True)
    product_uom_qty = fields.Float(string='Quantity', required=True, default=1.0,store=True)
    price_unit = fields.Float('Unit Price', required=True,default=0.0,store=True)
    tax_id=fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)],store=True)
    order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False,store=True)
    currency_id = fields.Many2one(related='order_id.currency_id', store=True, string='Currency', readonly=True)
    price_subtotal=fields.Monetary('Subtotal',store=True)
    product_uom=fields.Many2one("product.uom" , string='Unit Price',store=True)
    # purchase_price=fields.Float(string='Cost',store=True)

    
    
    # for order in self:
    #     for i in order.sale_line:
    #         print("====",i.saleorder_revise_count)
    
    # @api.multi
    # def write_sale(self,vals):
    #     revision_write={
    #         'sale_id':self.id,       
    #         'name':self.name,
    #         'partner_id':self.partner_id.id,
    #         'validity_date':self.validity_date,
    #         'payment_term_id':self.payment_term_id,
    #         'user_id':self.user_id.id,
    #         'client_order_ref':self.client_order_ref,
    #         'team_id':self.team_id.id,
    #         'date_order':self.date_order,
    #         'fiscal_position_id':self.fiscal_position_id.id,
    #         'origin':self.origin,
    #         'margin':self.margin,
    #         'partner_invoice_id':self.partner_invoice_id.id,
    #         'partner_shipping_id':self.partner_shipping_id.id,
    #         'pricelist_id':self.pricelist_id.id,
    #         'amount_untaxed':self.amount_untaxed,
    #         'amount_tax':self.amount_tax,
    #         'amount_total':self.amount_total
    #         }
    #     sale_order_obj=super(sale.order).write(revision_write)


  # @api.model
    # def create(self, vals):

    #     print('in super method')
    #     if vals.get('name', _('New')) == _('New'):
    #         if 'company_id' in vals:
    #             vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('sale.order') or _('New')
    #         else:
    #             vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or _('New')
            

    #     # if self.revise_order_count:
    #     #     self.revise_order_count=0
    #     # count=0
    #     # print('revise_order_count',self.revise_order_count)
    #     # count=self.revise_order_count+1
    #     # vals['revise_order_count']=count

    #     # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
    #     if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
    #         partner = self.env['res.partner'].browse(vals.get('partner_id'))
    #         addr = partner.address_get(['delivery', 'invoice'])
    #         vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
    #         vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
    #         vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist and partner.property_product_pricelist.id)
    #     result = super(inheritance_view_file, self).create(vals)
    #     return result
                
   
    # @api.depends('tax_line_id','order_line.price_total','order_line.price_unit','order_line.tax_id')
    # def _amount_all(self):
    #     """
    #     Compute the total amounts of the SO.
    #     """
    #     if self.tax_group_chkbox == 'False':
    #         for order in self:
    #             amount_untaxed = amount_tax = 0.0
    #             for line in order.order_line:
    #                 amount_untaxed += line.price_subtotal
    #                 amount_tax += line.price_tax
    #             order.update({
    #                 'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
    #                 'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
    #                 'amount_total': amount_untaxed + amount_tax,
    #             })
    #     else:
    #         for order in self:
    #             amount_untaxed = amount_tax = 0.0
    #             for line in order.order_line:
    #                 amount_untaxed += line.price_subtotal
    #                 price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
    #                 taxes=order.tax_line_id.compute_all(price,line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
    #                 price_tax=sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
    #             amount_tax += price_tax
    #             print(amount_untaxed,amount_tax)
    #             self.amount_untaxed=amount_untaxed
    #             self.amount_tax=amount_tax
    #             self.amount_total=amount_untaxed + amount_tax



    # for order in self:
            #     if order.sale_line:
            #         for i in order.sale_line:
            #             if i.saleorder_revise_count:
            #                 print("123456789")
            #                 i.saleorder_revise_count=0
            #             count=0
            #             count=i.saleorder_revise_count+3
            #             print("---------------->",count)
            #             vals['saleorder_revise_count']=count



            #  for order in self:
            #     for revise in order.sale_line:
            #         if revise.saleorder_revise_count:
            #             revise.saleorder_revise_count=0
            #     count=0
            #     print(' saleorder_revise_count', revise.saleorder_revise_count)
            #     count =revise.saleorder_revise_count+1
            #     vals['saleorder_revise_count']=count
