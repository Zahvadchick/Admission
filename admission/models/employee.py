# -*- coding: utf-8 -*-
from odoo import fields, models, api


"""class User(models.Model):
    _name = 'res.users'
    _inherit = ['res.users']

    employee = fields.Many2one('admission.employee',string='Контакт')"""


class Employee(models.Model):
    _name = 'admission.employee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Член комиссии'
                
    name = fields.Char(string="Имя сотрудника", required=True)
    email_id = fields.Char(string="Email")
    image = fields.Binary(string="Фотография", attachment=True)
    user_id = fields.Many2one(comodel_name = 'res.users', string='Контакт')
    color = fields.Integer(required=True)
    application_ids = fields.Many2many('admission.application', 'admission_application_rel', 'employee_id_rec',
                                       'application_id_rec',
                                        string='Назначенные заявления')

    def action_send_email(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = \
                ir_model_data.get_object_reference('mail_template', 'application_email_template')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'mail.template',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        }
        return {
            # 'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    '''@api.onchange('user_id')
    def _change_fields(self):
        print("hello")
        self.user_id.update({
            'employee': self.id
        })'''