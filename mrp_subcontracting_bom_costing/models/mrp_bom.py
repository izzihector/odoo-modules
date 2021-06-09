from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tools import float_round

class MrpBom(models.Model):
    _inherit = "mrp.bom"

    child_ids = fields.One2many('mrp.bom', 'parent_id', string="Child Bill of Materials", help="")
    parent_id = fields.Many2one('mrp.bom', string="Father Bill of Materials", help="")
    cost_weight = fields.Float("Cost weight", default=1)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You can not create recursive relationships between BoMs.'))
        if self.parent_id and self.child_ids:
            raise ValidationError(_('BoM relationships cannot be multi layered.'))

class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    def _get_bom(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False):
        lines = super(ReportBomStructure, self)._get_bom(bom_id, product_id, line_qty, line_id, level)
        lines['deferrable_costs'] = 0
        lines['absorbable_costs'] = 0

        bom = self.env['mrp.bom'].browse(bom_id)
        relative_boms = self.env['mrp.bom'].search(['&', ('id', '!=', bom_id),
                                                    '|', ('id', '=', bom.parent_id.id),
                                                         ('id', 'in', bom.child_ids.ids  + bom.parent_id.child_ids.ids)])

        if relative_boms:
            own_weight = bom.cost_weight
            other_weight = sum(relative_boms.mapped('cost_weight'))
            
            deferrable_costs = lines['operations_cost']*other_weight/(other_weight + own_weight)
            lines['total'] -= deferrable_costs
            lines['deferrable_costs'] = -deferrable_costs

            absorbable_costs = 0
            factor = line_qty/bom.product_qty
            for routing in relative_boms.mapped('routing_id'):
                operation_cycle = float_round(factor, precision_rounding=1, rounding_method='UP')
                operations = self._get_operation_line(routing, operation_cycle, 0)
                absorbable_costs += sum([op['total'] for op in operations])

            lines['absorbable_costs'] = absorbable_costs*own_weight/(other_weight + own_weight)
            lines['total'] += lines['absorbable_costs']


        return lines

    def _get_price(self, bom, factor, product):
        price = super(ReportBomStructure, self)._get_price(bom, factor, product)

        relative_boms = self.env['mrp.bom'].search(['&', ('id', '!=', bom.id),
                                                    '|', ('id', '=', bom.parent_id.id),
                                                         ('id', 'in', bom.child_ids.ids  + bom.parent_id.child_ids.ids)])

        if relative_boms:
            own_weight = bom.cost_weight
            other_weight = sum(relative_boms.mapped('cost_weight'))

            operation_cycle = float_round(factor, precision_rounding=1, rounding_method='UP')
            operations = self._get_operation_line(bom.routing_id, operation_cycle, 0)
             

            deferrable_costs = sum([op['total'] for op in operations])*other_weight/(other_weight + own_weight)
            price -= deferrable_costs


        return price