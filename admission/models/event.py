from datetime import timedelta, datetime
from odoo import models, fields, api


class Event(models.Model):
    _name = 'admission.event'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Application events"

    name = fields.Char(string = "Тема", required = True)
    description = fields.Text(string="Описание встречи")
    event_time = fields.Date(string="Дата события", required = True)
    color = fields.Integer()
    application_id = fields.Many2one(comodel_name='admission.application', string='Заявление, связанное с событием')
    employee_ids = fields.Many2many('admission.employee', 'event_employee_rel', 'event_id_rec',
                                    'employee_id_rec',
                                    string='Проверяющие')
