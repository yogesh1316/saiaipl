from odoo import api,fields,models, _
from odoo.exceptions import UserError,ValidationError

#Text Master   
class text_master_information(models.Model):
    _name='text_master.info'
    _rec_name='text_description'
    _sql_constraints = [('Unique Text','unique(text_concat)','Please Enter Unique Text Description.')]
        
    text_code=fields.Char(string='Text Code')
    text_description = fields.Char('Text Description',required=True)
    text_concat = fields.Char("Text Concat",compute='text_concate_fun',store=True)
    
    #Unique Text
    @api.depends('text_description')
    def text_concate_fun(self):
        text_data_str=str(self.text_description).lower()
        self.text_concat=text_data_str.replace(' ','')

    @api.model
    def create(self,values):
        if values:
            values["text_code"] = self.env['ir.sequence'].next_by_code('text_master.info')
            if values['text_description']:
                print(values)
                if values['text_description'].replace(' ','')=='':
                    raise UserError(_("Please Enter Text Description."))
                else:
                    return super(text_master_information,self).create(values)
         
         
    @api.multi
    def write(self,values):
        if values['text_description']:
            if values['text_description'].replace(' ','')=='':
                raise UserError(_("Please Enter Text Description."))
            else:
                return super(text_master_information,self).write(values)

#Effect Master
class effect_master_info(models.Model):
    _name='effect_master.info'
    _rec_name='effect_description'
    _sql_constraints =[('Unique Effect','unique(unique_effect_description)','Please Enter Unique Effect Description.')]
    effect_code_no =fields.Char(string='Effect Code.',readonly=True)
                            
    effect_description=fields.Char('Effect Description',required=True)
    unique_effect_description=fields.Char('Unique Effect Description',compute='effect_concate_compute' ,store=True)
    
    #Unique Effect
    @api.depends('effect_description')
    def effect_concate_compute(self):
        text_effe_data=str(self.effect_description).lower()
        self.unique_effect_description=text_effe_data.replace(' ','')
        
        
        
    @api.model
    def create(self,values):
        if values:
            values['effect_code_no']=self.env['ir.sequence'].next_by_code('effect_master.info')
            if values['effect_description']:
                if values['effect_description'].replace(' ','')=='':
                    raise UserError(_("Please Enter Effect Description."))
                else:
                    return super(effect_master_info,self).create(values)

    @api.multi
    def write(self,values):
        if values['effect_description']:
            if values['effect_description'].replace(' ','')=='':
                raise UserError(_("Please Enter  Effect Description."))
            else:
                return super(effect_master_info,self).write(values)
 #ID Code Master
class id_code_master_info(models.Model):
    _name='id_code_master.info'
    _rec_name='id_code_description'
    _sql_constraints =[('Unique Id Code','unique(unique_id_code_description)','Please Enter Unique Id Description')]
    id_code_no =fields.Char('Id No.',readonly=True)
    
    id_code_description=fields.Char("Id Description",required=True)
    unique_id_code_description=fields.Char("Unique Id Description",compute='id_decription_concat_fun' ,store=True)
    
    #Unique ID Code
    @api.depends('id_code_description')
    def id_decription_concat_fun(self):
        id_code_data=str(self.id_code_description).lower()
        self.unique_id_code_description=id_code_data.replace(' ','')
        
    @api.model
    def create(self,values):
        if values:
            values['id_code_no']=self.env['ir.sequence'].next_by_code('id_code_master.info')
            if values['id_code_description']:
                if values['id_code_description'].replace(' ','')=='':
                    raise UserError(_("Please Enter Id Description."))
                else:
                    return super(id_code_master_info,self).create(values)

    @api.multi
    def write(self,values):
        if values['id_code_description']:
            if values['id_code_description'].replace(' ','')=='':
                raise UserError(_("Please Enter Id Description."))
            else:
                return super(id_code_master_info,self).write(values)
 
#Make Master
class make_master_info(models.Model):
    _name='make_master.info'
    _rec_name='make_description'
    _sql_constraints=[('Unique Make No.','unique(unique_make_description)','Please Enter Unique Make Description.')]
    make_no=fields.Char('Make No.',readonly=True)
    make_description=fields.Char('Make Description',required=True)
    unique_make_description=fields.Char('Unique Make Description',compute='make_master_concat_fun',store=True)

    #Unique Make 
    @api.depends('make_description')
    def make_master_concat_fun(self):
        make_data=str(self.make_description).lower()
        self.unique_make_description=make_data.replace(' ','')
    
    @api.model
    def create(self,values):
        if values:
            values['make_no']=self.env['ir.sequence'].next_by_code('make_master.info')
            if values['make_description']:
                if values['make_description'].replace(' ','')=='':
                    raise UserError(_("Please Enter Make Description."))
                else:
                    return super(make_master_info,self).create(values)
            
    @api.multi
    def write(self,values):
        if values['make_description']:
            if values['make_description'].replace(' ','')=='':
                raise UserError(_("Please Enter Make Description."))
            else:
                return super(make_master_info,self).write(values)
        
#MRP Type Master        
class mrp_type_master_info(models.Model):
    _name='mrp_type_master.info'
    _rec_name='mrp_description'
    _sql_constraints=[('Unique MRP Type Code.','unique(unique_mrp_description)','Please Enter Unique MRP Type Description.')]
    mrp_type_code=fields.Char('MRP Type Code',required=True)
    mrp_description=fields.Char('MRP Type Description',required=True)
    unique_mrp_description=fields.Char('Unique MRP Type Description',compute='mrp_type_description_fun',store=True)
    
    # Unique MRP Type
    @api.depends('mrp_description')
    def mrp_type_description_fun(self):
        mrp_desc_str_data=str(self.mrp_description).lower()
        self.unique_mrp_description=mrp_desc_str_data.replace(' ','')
    
    @api.model
    def create(self,values):
        if values['mrp_description']:
            if values['mrp_description'].replace(' ','')=='':
                raise UserError(_("Please Enter MRP Type Description."))
            else:
                return super(mrp_type_master_info,self).create(values)
                
    @api.multi
    def write(self,values):
        if values['mrp_description']:
            if values['mrp_description'].replace(' ','')=='':
                raise UserError(_("Please Enter MRP Type Description."))
            else:
                return super(mrp_type_master_info,self).write(values)

#Source Master
class source_master_info(models.Model):
    _name='source_master.info'   
    _rec_name='source_description'         
    _sql_constraints=[('Unique Source Description','unique(unique_source_description)','Please Enter Unique Source Description.')]
    source_code=fields.Char('Source Code',required=True)
    source_description=fields.Char('Source Description',required=True)
    unique_source_description=fields.Char('Unique Source Description',compute='source_description_fun',store=True)
    
    # Unique Source 
    @api.depends('source_description')
    def source_description_fun(self):
        sourc_desc_str_data=str(self.source_description).lower()
        self.unique_source_description=sourc_desc_str_data.replace(' ','')
        
    @api.model
    def create(self,values):
            if values['source_description']:
                if values['source_description'].replace(' ','')=='':
                    raise UserError(_("Please Enter Source Description."))
                else:
                    return super(source_master_info,self).create(values)
                
    @api.multi
    def write(self,values):
        if values['source_description']:
            if values['source_description'].replace(' ','')=='':
                raise UserError("Please Enter Source Description.")
            else:
                return super(source_master_info,self).write(values)

#HSN Master            
class hsn_master_info(models.Model):
    _name='hsn_master.info'
    
    _rec_name='hsn_no'
    hsn_no=fields.Char("HSN No.",required=True)
    _sql_constraints=[('Unique HSN No.','unique(hsn_no)','Please Enter Unique HSN No.')] #Unique HSN Number

    rate=fields.Char("Rate")
    in_state_sale=fields.Many2one('account.tax',string='In state sale')
    out_state_sale=fields.Many2one('account.tax',string='Out state sale')
    in_state_purchase=fields.Many2one('account.tax',string='In state purchase')
    out_state_purchase=fields.Many2one('account.tax',string='Out state purchase')
    
    #HSN Number only Numeric
    @api.constrains('hsn_no')
    def chk_hsn_number(self):
        if self.hsn_no.isdigit():
            pass
        else:
            raise ValidationError(_('Please Enter Only Number.'))
                
        
        
    @api.model
    def create(self,values):
        if values['hsn_no']:
            if values['hsn_no'].replace(' ','')=='':
                raise UserError(_("Please Enter HSN Number."))
        if values['rate']:
                if values['rate']< str(0):
                    raise UserError(_("Do not Enter Negative Rate "))
                else:
                    raise UserError(_("Do not Enter Text,Please Enter Number."))
        return super(hsn_master_info,self).create(values)
    
    @api.multi
    def write(self,values):
        if "hsn_no" in values:
            if values['hsn_no']:
                if values['hsn_no'].replace(' ','')=='':
                    raise UserError(_("Please Enter HSN Number."))
                else:
                    return super(hsn_master_info,self).write(values)
    
    @api.onchange('rate')
    def hsn_master_rate(self):
        temp=""
        obj_acc_tax=self.env['account.tax']
        if self.rate:
            
            temp="GST "+self.rate+"%"
            search1=obj_acc_tax.search([('amount_type','=','group'),('type_tax_use','=','sale'),('name','=',temp)])
            self.in_state_sale=search1     
                   
            temp="IGST "+self.rate+"%"
            search2=obj_acc_tax.search([('amount_type','=','percent'),('type_tax_use','=','sale'),('name','=',temp)])
            self.out_state_sale=search2
            
            temp="GST "+self.rate+"%"
            search3=obj_acc_tax.search([('amount_type','=','group'),('type_tax_use','=','purchase'),('name','=',temp)])
            self.in_state_purchase=search3
            
            temp="IGST "+self.rate+"%"
            search4=obj_acc_tax.search([('amount_type','=','percent'),('type_tax_use','=','purchase'),('name','=',temp)])
            self.out_state_purchase=search4
    

     
    
    
    
    
    
    
    
    