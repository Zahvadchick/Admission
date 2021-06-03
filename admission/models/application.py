# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from odoo import models, fields, api


class CustomModelPoint(models.Model):
    _name = 'custom.model.point'

    employee_id = fields.Many2one('admission.employee', string = 'Сотрудник, выставивший оценку')
    number = fields.Integer(string = 'Оценка')


AVAILABLE_PRIORITIES = [
    ('0', 'Very Low'),
    ('1', 'Низкий'),
    ('2', 'Средний'),
    ('3', 'Высокий'),
    ('4', 'Крайне высокий')]

class Application(models.Model):
    _name = 'admission.application'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Admission Applications"

    name = fields.Char(string = "Абитуриент", required = True, help = "Имя абитуриента, подавшего заявление")
    description = fields.Text(string="Описание")
    image = fields.Binary(string="Фотография", attachment=True)
    email_id = fields.Char(string="Email")
    start_date = fields.Date(string="Принята", readonly = True, default=fields.Date.today)
    deadline = fields.Date(string="Дедлайн")
    link = fields.Char(string="Ссылка на гугл диск")
    color = fields.Integer()
    documents = fields.Many2many("ir.attachment", "attach_rel",
                                 "m2m_id", "attachment_id3", string="Вложения",)
    state = fields.Selection([
        ('na', 'Нераспределенные'),
        ('primary rejected', 'Первично отбракованные'),
        ('primary accepted', 'Первично поступившие'),
        ('reviewed by the curator', 'Рассмотренние куратором'),
        ('reviewed by the members of the commission', 'Рассмотренние членами комиссии'),
        ('additional actions are required', 'Требуются дополнительные действия'),
        ('reviewed', 'Рассмотренные'),
        ('added to ACAB', 'Внесено в ACAB'),
        ('closed', 'Закрытые'),
    ], required = True, default = 'na', string="Статус", group_expand='_expand_states', index=True)
    set_priority = fields.Selection(AVAILABLE_PRIORITIES, string = "Приоритет")
    set_tags = fields.Many2many(comodel_name='custom.model.tags', string="Теги")
    set_points = fields.Many2many(comodel_name='custom.model.point', string="Оценки")
    employee_ids = fields.Many2many('admission.employee', 'admission_application_rel', 'application_id_rec',
                                    'employee_id_rec',
                                  string='Проверяющие')
    progress = fields.Selection([
        ('assigned', 'Назначается'),
        ('in progress', 'В процессе'),
        ('done', 'Закрыта')],
        required = True,
        default = 'assigned')

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

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
            #'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def button_assigned(self):
        for rec in self:
            rec.write({'progress': 'in progress'})
        for emp in self.employee_ids:
            #self.env['custom.model.point'].sudo().create({
                #'employee_id ': emp
            #})
            template_id = self.env.ref('admission.application_email_template').id
            template = self.env['mail.template'].browse(template_id)
            template.write({'email_to': emp.email_id})
            template.send_mail(self.id, force_send=True)

    @api.onchange('state')
    def change_fields(self):
        for rec in self:
            rec.write({'progress': 'assigned'})


class CustomModelTags(models.Model):
    _name = 'custom.model.tags'

    name = fields.Char(required = True)
    color = fields.Integer()


class Attachment(models.Model):
    _inherit = 'ir.attachment'

    attach_rel = fields.Many2many("admission.application", "documents", "attachment_id3", "m2m_id",string="Attachment", invisible=1 )
