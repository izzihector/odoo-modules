from odoo import fields, models, api
from odoo.exceptions import ValidationError

from datetime import datetime
from dateutil import relativedelta

class WebhookValidationError(ValidationError):
    pass

class MrpWorkcenter(models.Model):
    _inherit = "mrp.workcenter"

    def get_latest_loss(self, user_id=False, workorder_id=False, open_only=True, loss_type=False, limit=1):
        self.ensure_one()

        domain = [('workcenter_id', '=', self.id)]

        if workorder_id:
            domain.append(('workorder_id', '=', False))

        if open_only:
            domain.append(('date_end', '=', False))
        
        if loss_type:
            domain.append(('loss_type', '=', loss_type))

        if user_id:
            domain.append(('user_id', '=', user_id))

        loss = self.env['mrp.workcenter.productivity'].search(domain, limit=limit)

        return loss


    def log(self, dt, **kwargs):
        self.ensure_one()

        user_id, workorder_id, loss_id = kwargs.get('user_id', False) and int(kwargs.get('user_id')),           \
                                         kwargs.get('workorder_id', False) and int(kwargs.get('workorder_id')), \
                                         kwargs.get('loss_id', False) and int(kwargs.get('loss_id'))

        
        loss = self.get_latest_loss(user_id, workorder_id)
        loss_id_rec = self.env['mrp.workcenter.productivity.loss'].browse(loss_id)
        
        if loss and not loss.date_end:
            if (loss_id_rec.loss_type in ['productive', 'scrap']) and (loss.loss_id.loss_type == loss_id_rec.loss_type):
                self.env['mrp.workcenter.productivity.timestamp'].create({'productivity_log_id': loss.id, 'timestamp': fields.Datetime.now()})
                return

            else: 
                loss.date_end = dt
        
        now = datetime.now()
        working_time = self.resource_calendar_id.get_work_duration_data(now, now + relativedelta.relativedelta(minutes=1))
        
        if not working_time or working_time.get('hours', 0) == 0:
            return

        workorder = workorder_id and self.env['mrp.workorder'].browse(workorder_id) or self.env['mrp.workorder'].search([('state', '=', 'progress'), ('workcenter_id', '=', self.id), ('mes_ignore', '=', False)])

        loss = loss.create({'workcenter_id': self.id, 'workorder_id': workorder_id or workorder.id, 
                                'date_start': dt, 'date_end': False, 'loss_id': loss_id, 'user_id': user_id, 
                                'company_id': workorder_id and workorder_id.company_id.id or 1})

    def update_latest(self, **kwargs):
        self.ensure_one()

        user_id, workorder_id, loss_id = kwargs.get('user_id', False) and int(kwargs.get('user_id')),           \
                                         kwargs.get('workorder_id', False) and int(kwargs.get('workorder_id')), \
                                         kwargs.get('loss_id', False) and int(kwargs.get('loss_id'))

        loss = self.get_latest_loss(user_id, workorder_id, open_only=False, loss_type=kwargs.get('loss_type', False), limit=1)

        if loss:
            loss.write({'loss_id': loss_id})

    #critical_oee = fields.Float(string="Critical Efficiency", help="Used in efficiency control. If efficiency is than this percentage, shutdown will be reccomended.")