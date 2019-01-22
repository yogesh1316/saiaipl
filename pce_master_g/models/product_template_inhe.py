from odoo import api,fields,models, _
from odoo.exceptions import UserError,ValidationError




class product_template_inhe(models.Model):
    _inherit='product.template'
    _sql_constraints=[('Unique Product Name','unique(unique_product)','Please Enter Unique Product Name.')]

    item_code_num =fields.Char(string='Id Code No.',store=True)
    drawing_number =fields.Char('Drawing Number.')
    
    
    text_master_id=fields.Many2one('text_master.info',string='Text',required=True)
    effect_code_description=fields.Many2one('effect_master.info',string='Effect Code Descrip.',required=True)      
    id_code_description=fields.Many2one('id_code_master.info',string="Id Code Descrip.",required=True)
    manufacturer=fields.Many2one('make_master.info',string='Manufacturer',required=True)
    mrp_type=fields.Many2one('mrp_type_master.info',string='MRP Type',required=True)#,compute='mrp_type_fun'
    source_code_master=fields.Many2one('source_master.info',string='Source Code',required=True)
   # hsn_num_master=fields.Many2one('hsn_master.info',string='HSN No.',required=True)
    mf_part_no=fields.Char(string='Mf. Part No.')
    attach_pdf=fields.Binary(string='Attach Pdf')
    filename=fields.Char()
    batch_qty=fields.Float(string='Batch Qty.',required=True ,default=0.0)
    reorder_level=fields.Float(string='ReOrder Level',required=True,default=0.0)
    lead_time=fields.Integer(string='Lead Time')
    buyer_code=fields.Many2one('res.users',string='Buyer Code',required=True)
    bin_location=fields.Char(string='Bin Location')
    bulk_issue_flag=fields.Selection([('yes','Yes'),('no','No')],'Bulk Issue Flag')
    channel_flag=fields.Selection([('red','Red'),('green','Green')],'Channel Flag')
    sr_no_application=fields.Selection([('yes','Yes'),('no','No')],'SrNo.Application')
    unique_product=fields.Char(string="Unique Product Name",compute='unique_product__name_fun',store=True)

    @api.depends('name')
    def unique_product__name_fun(self):
        for i in self:
            text_data_uuustr=str(i.name).lower()
            i.unique_product=text_data_uuustr.replace(' ','')
     
    @api.onchange('mrp_type')
    def mrp_type_onchange(self):
        if self.mrp_type:
            self.batch_qty=0
            self.reorder_level=0

    @api.constrains('reorder_level','batch_qty')
    def check_batch_qty_reorder_level(self):
        if self.mrp_type.unique_mrp_description=='requirementbase':
            if self.batch_qty>0:
                raise ValidationError("Enter Batch Qty. Less than One")
            if self.reorder_level>0:
                raise ValidationError(_("Enter Reorder Level Less than One."))
            if self.batch_qty<0:
                raise ValidationError(_("Please Do Not Enter Negative Number."))
            if self.reorder_level<0:
                raise ValidationError(_("Please Do Not Enter Negative Number."))

        if self.mrp_type.unique_mrp_description=='consumptionbase' or self.mrp_type.unique_mrp_description=='criticalbase':
            if self.batch_qty==0:
                raise ValidationError("Enter Batch Qty. Greater than Zero")
            if self.reorder_level==0:
                raise ValidationError(_("Enter Reorder Level Greater than Zero."))
            if self.batch_qty<0:
                raise ValidationError(_("Please Do Not Enter Negative Number."))
            if self.reorder_level<0:
                raise ValidationError(_("Please Do Not Enter Negative Number."))
        
        if self.mrp_type.unique_mrp_description=='batchquantity':
            if self.batch_qty==0:
                raise ValidationError("Enter Batch Qty. Greater than Zero")
            if self.reorder_level>0:
                raise ValidationError(_("Enter Reorder Level Less than One."))
            if self.batch_qty<0:
                raise ValidationError(_("Please Do Not Enter Negative Number."))
            if self.reorder_level<0:
                raise ValidationError(_("Please Do Not Enter Negative Number."))
    
    @api.constrains('mrp_type')
    def check_batch_qty(self):
        if self.mrp_type.unique_mrp_description=='consumptionbase':
                if self.batch_qty==0:
                    raise ValidationError("Enter Batch Qty. greater than Zero")

                if self.reorder_level==0:
                    raise ValidationError("Enter Reorder Level Greater than Zero.")

        if self.mrp_type.unique_mrp_description=='criticalbase':
                if self.batch_qty==0:
                    raise ValidationError("Enter Batch Qty. greater than Zero")

                if self.reorder_level==0:
                    raise ValidationError("Enter Reorder Level Greater than Zero.")

        if self.mrp_type.unique_mrp_description=='batchquantity':
                if self.batch_qty==0:
                    raise ValidationError("Enter Batch Qty. greater than Zero")
                if self.batch_qty<0:
                    raise ValidationError(_("Please Do Not Enter Negative Number."))
                if self.reorder_level>0:
                    raise ValidationError("Enter Reorder Level Less than One.")
                if self.reorder_level<0:
                    raise ValidationError(_("Please Do Not Enter Negative Number."))
    @api.model
    def create(self, vals):
        rmp_type_obj=self.env['mrp_type_master.info']

        if vals:
            vals['item_code_num'] = self.env['ir.sequence'].next_by_code('product.template') 
            if vals['drawing_number']==False:
                vals['drawing_number']=vals['item_code_num']

            if 'mrp_type' in vals:
                mrp=rmp_type_obj.search([('id','=',vals['mrp_type'])])
                if mrp.unique_mrp_description =='requirementbase':  

                         if vals['batch_qty']>0 or vals['reorder_level']>0 or vals['batch_qty']<0 or vals['reorder_level']<0:
                             raise UserError(_("Enter Batch Qty.And Reorder Level Less than One."))
                         if vals['batch_qty']<0:
                             raise UserError(_("Please Do Not Enter Negative Number."))
                         if vals['reorder_level']<0:
                             raise UserError(_("Please Do Not Enter Negative Number."))
                if mrp.unique_mrp_description =='consumptionbase' or mrp.unique_mrp_description =='criticalbase':
                    if vals['batch_qty']==0 or vals['reorder_level']==0 or vals['batch_qty']<0 or vals['reorder_level']<0:
                            raise UserError(_("Enter Batch Qty. and Reorder Level Greater than Zero."))
                    elif vals['batch_qty']<0 or vals['reorder_level']<0:
                            raise UserError(_("Please Do Not Enter Negative Number."))
                if mrp.unique_mrp_description =='batchquantity':
                    if vals['batch_qty']==0 or  vals['batch_qty']<0:
                            raise UserError(_("Enter Batch Qty. Greater than Zero."))
                    if vals['reorder_level']>0 or vals['reorder_level']<0:
                            raise UserError(_("Enter Reorder Level. Less than One."))
                    elif vals['batch_qty']<0 or vals['reorder_level']<0:
                            
                            raise UserError(_("Please Do Not Enter Negative Number."))
        if vals['name']:
            if vals['name'].replace(' ','')=='':
                raise UserError(_("Please Enter Product  Name."))
        if 'lead_time' in vals:
            if vals['lead_time']<0:
                raise UserError(_("Please Do Not Enter Negative Lead Time.")) 
            
            else:
                return super(product_template_inhe, self).create(vals)
    
    
    @api.multi
    def write(self,values):
        if values:
            if 'name' in values:
                if values['name'].replace(' ','')=='':
                    raise UserError(_("Do not Enter Empty Product"))
            if 'lead_time' in values:
                if values['lead_time']<0:
                    raise UserError(_("Please Do Not Enter Negative Lead Time.")) 
        return super(product_template_inhe, self).write(values)
    
    
    
    
    
    
    
    
    


