from odoo import http
from odoo.http import request
import base64

class Admission(http.Controller):

    @http.route('/application_webform', type="http", auth="public", website=True)
    def application_webform(self, **post):
        return http.request.render('admission.create_application', {})

    @http.route('/create/webapplication', type="http", auth="public", website=True)
    def create_webapplication(self, **post):
        #request.env['admission.application'].sudo().create(post)
        application = request.env['admission.application'].sudo().create({
            'name': post.get('name'),
            'email_id': post.get('email_id')
        })
        for ths in [post.get('file_1'), post.get('file_2'), post.get('file_3'), post.get('file_4'), post.get('file_5'),
                    post.get('file_6'), post.get('file_7'), post.get('file_8'), post.get('file_9')]:
            if ths:
                attachments = request.env['ir.attachment']
                file_name = ths.filename
                file = ths
                attachment_id = attachments.create({
                    'name': file_name,
                    'type': 'binary',
                    'datas': base64.b64encode(file.read()),
                    'res_model': 'model.model',
                    'res_id': application.id
                })
                application.update({
                    'documents': [(4, attachment_id.id)],
                })
        image = post.get('img')
        application.update({
            'image': base64.b64encode(image.read())
        })
        """attachments = request.env['ir.attachment']
        file_name = post.get('img').filename
        file = post.get('img')
        attachment_id = attachments.create({
            'name': file_name,
            'type': 'binary',
            'datas': base64.b64encode(file.read()),
            'res_model': 'model.model',
            'res_id': application.id
        })
        application.update({
            'image': attachment_id.id
        })"""
        return request.render("admission.applicant_thanks", {})
