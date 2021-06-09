# Part of <Odoo Addons for RDS Moulding Technology S.p.A.>. See Attached README.md file.
# Copyright 2018 RDS Moulding Technology S.p.A.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp

class MrpWorkcenterProductivityLossType(models.Model):
    _inherit = "mrp.workcenter.productivity.loss.type"
    _rec_name = 'name'

    @api.depends('name')
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, rec.name))
        return result
    
    name = fields.Char("Category", required="True")
    loss_type = fields.Selection(selection_add=[('undefined_loss', 'Undefined Loss'),('scrap', 'Scrap')])

class MrpWorkcenterProductivityLoss(models.Model):
    _inherit = "mrp.workcenter.productivity.loss"

    color = fields.Char("Andon / Graph Color")
    no_oee = fields.Boolean("Exclude from OEE Calculation")
    loss_id = fields.Many2one(domain=([]))

class MrpWorkcenterProductivityTimestamp(models.Model):
    _name = "mrp.workcenter.productivity.timestamp"
    _description = "MRP Productivity Log Timestamp"
    _order = "timestamp desc"

    timestamp = fields.Datetime("Timestamp")
    productivity_log_id = fields.Many2one('mrp.workcenter.productivity', ondelete='cascade')

class MrpWorkcenterProductivity(models.Model):
    _inherit = "mrp.workcenter.productivity"

    timestamp_ids = fields.One2many('mrp.workcenter.productivity.timestamp', 'productivity_log_id', "Logged Cycles")

"""
class MrpWorkcenterProductivity(models.Model):
    _inherit = "mrp.workcenter.productivity"

    employee_id = fields.Many2one('hr.employee', string='Employee')
   
    time_cycle_nominal = fields.Float(compute="_compute_efficiency", string="Nominal Time Cycle", group_operator="avg", store=True)
    qty_produced = fields.Float(string="Quantity Produced", digits=dp.get_precision('Product Unit of Measure'))

    time_cycle = fields.Float(string="Time Cycle", group_operator="avg", compute="_compute_efficiency", store=True)
    efficient_duration = fields.Float(string="Efficient Time", compute="_compute_efficiency", store=True)

    efficiency_mode = fields.Selection([('standard', 'Odoo Standard'),
                                        ('interval', 'Avg per Interval')], default='standard', required=True, string="Production Control Type", related="workcenter_id.efficiency_mode")


    @api.depends('loss_type', 'workorder_id', 'workorder_id.operation_id', 'workorder_id.operation_id.time_cycle', 'workcenter_id', 'workcenter_id.efficiency_mode', 'qty_produced', 'duration', 'date_end')
    def _compute_efficiency(self):
        for i in self:
            if not i.workorder_id:
                continue
                
            i.time_cycle_nominal = i.workorder_id.operation_id.time_cycle

            if i.loss_type != 'productive':
                i.efficienct_duration = 0

            elif (i.efficiency_mode == 'standard'):
                i.efficient_duration = i.duration

            elif i.qty_produced > 0:
                i.efficient_duration = i.qty_produced * i.time_cycle_nominal / i.workorder_id.bom_id.product_qty
                i.time_cycle = i.duration * i.workorder_id.bom_id.product_qty / i.qty_produced

            else:
                i.efficient_duration = i.time_cycle = 0

    def merge(self):
        k = None
        date_start_buffer = False
        qty_produced_buffer = 0
        description_buffer = ""

        to_unlink = self.env['mrp.workcenter.productivity']


        for i in self:
            if not k:
                k = i
                date_start_buffer = i.date_start
                qty_produced_buffer = i.qty_produced
                description_buffer = i.description or ""
                continue

            if k.is_contiguous(i) or i.date_end != date_start_buffer:
                date_start_buffer = i.date_start
                qty_produced_buffer += i.qty_produced
                description_buffer = description_buffer + (i.description and ("\n %s" % i.description) or "")
                to_unlink += i
            
            else:
                if to_unlink:
                    k.write({'date_start': date_start_buffer, 'qty_produced': qty_produced_buffer, 'description': description_buffer})
                    to_unlink.unlink()
                    to_unlink = self.env['mrp.workcenter.productivity']

                k = i
                date_start_buffer = i.date_start
                qty_produced_buffer = i.qty_produced
                description_buffer  = i.description or ""

        
        if self[-1] != k:
            k.write({'date_start': date_start_buffer, 'qty_produced': qty_produced_buffer, 'description': description_buffer})
            self[-1].unlink()
            

    def is_contiguous(self, i):
        return (self.loss_id.id == i.loss_id.id) and (self.workorder_id.id == i.workorder_id.id)
"""