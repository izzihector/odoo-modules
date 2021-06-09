# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class WorkorderOverproduceConfirmWizard(models.TransientModel):
    _name = 'workorder.overproduce.confirm.wizard'
    _description = 'Overproduce Confirmation'

    def confirm(self):
        workorder = self.env['mrp.workorder'].browse(self.env.context.get('workorder_id')).with_context(overproduce=True)

        self.env['change.production.qty'].with_context(skip_activity=True).create({
            'mo_id': workorder.production_id.id,
            'product_qty': workorder.qty_produced + workorder.qty_producing
        }).change_prod_qty()

        return workorder.record_production()