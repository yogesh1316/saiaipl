from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


# create_by | create_date | update_by | update_date
# Ganesh      11/10/2018                
# Info : This master model is use to identify why item get rejected for that reason is reqired 

class reason_master(models.Model):
    _name='reason.master'   
    _rec_name='reason_desc'    
         
    _sql_constraints=[('Unique Reason Description','unique(unique_reason_desc)','Please Enter Unique Reason Description.')]
    reason_desc=fields.Char('Reason Description',required=True,help="Please Enter Unique Description")
    unique_reason_desc=fields.Char('Unique Reason Description' ,compute='reason_description_fun',store=True)

    #Unique Reason Description
    @api.depends('reason_desc')
    def reason_description_fun(self):
        desc_str_data=str(self.reason_desc).lower()
        self.unique_reason_desc=desc_str_data.replace(' ','')
      
    @api.model
    def create(self,values):
            if values['reason_desc']:
                if values['reason_desc'].replace(' ','')=='':
                    raise UserError(_("Please Enter Reason Description."))
                else:
                    return super(reason_master,self).create(values)

    @api.multi
    def write(self,values):
        if values['reason_desc']:
            if values['reason_desc'].replace(' ','')=='':
                raise UserError("Please Enter Reason Description.")
            else:
                return super(reason_master,self).write(values)
