
from odoo import api, models, _
from odoo.exceptions import UserError

class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = 'product.product'
    _description = 'Product'

    def _compute_bom_price(self, bom, boms_to_recompute=False):
        price = super(ProductProduct, self)._compute_bom_price(bom, boms_to_recompute)

        relative_boms = self.env['mrp.bom'].search(['&', ('id', '!=', bom.id),
                                                    '|', ('id', '=',  bom.parent_id.id),
                                                    ('id', 'in', bom.child_ids.ids + bom.parent_id.child_ids.ids)])

        if not relative_boms:
            return price

        total = self.uom_id._compute_price(price * bom.product_qty, bom.product_uom_id)
        
        own_weight = bom.cost_weight
        other_weight = sum(relative_boms.mapped('cost_weight'))

        for opt in bom.routing_id.operation_ids:
            duration_expected = (
                opt.workcenter_id.time_start +
                opt.workcenter_id.time_stop +
                opt.time_cycle)
            total -= ((duration_expected / 60) * opt.workcenter_id.costs_hour)*other_weight/(other_weight + own_weight)

        absorbable_factor = own_weight/(other_weight + own_weight)
        for opt in relative_boms.mapped('routing_id').mapped('operation_ids'):
            duration_expected = (
                opt.workcenter_id.time_start +
                opt.workcenter_id.time_stop +
                opt.time_cycle)
            total += (duration_expected / 60) * opt.workcenter_id.costs_hour *  absorbable_factor

        return bom.product_uom_id._compute_price(total / bom.product_qty, self.uom_id)