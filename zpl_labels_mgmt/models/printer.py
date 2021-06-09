# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
import datetime
import re, time, socket
from lxml import etree
from odoo.exceptions import UserError

class ZPLPrinter(models.Model):
    _name = 'zpl.printer'
    _description = "ZPL Printer"

    name = fields.Char('Nome', required=True)
    address = fields.Char('Indirizzo', required=True)
    port = fields.Integer('Porta', required=True)

    size_code = fields.Char("Label Type Code")
    
    def _print(self, zpl):
        
        errors = 0
        import logging
        logging.warning(zpl)
        while True:
            try:
                logging.warning(zpl)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           
                s.connect((self.address, self.port))
                s.send(zpl)
                s.close()
                time.sleep(0.2)
                errors = 0
                break
            
            except Exception as e:
                
                time.sleep(1)
                errors += 1
                if errors >= 5:
                    raise UserError("La stampante sembra essere in errore\n{}: {}".format(e.__class__.__name__, e))

    def action_print(self, format_id, records, copies=0):
        if copies == 0:
            action = self.env.ref('zpl_labels_mgmt.action_zpl_wizard').read()[0]
            #wiz = self.env['zpl.wizard.simple'].create({})
            #action['res_id']  = wiz.id,
            action['context'] = {'format_id': format_id, 'record_name': records._name, 
                                    'record_ids': records.ids, 'printer_id': self.id}

            return action

        format_id = self.env['zpl.format'].browse(format_id)

        if format_id.size_code != self.size_code:
            valid_fallback = format_id.fallback_formats.filtered(lambda x: x.size_code == self.size_code)
            format_id = valid_fallback or format_id

        count = 0

        if format_id.type == "multi":
            printed_labels = 0
            while printed_labels < copies:
                zpl = format_id.compile(records, count)
                printed_labels += 1
                count += 1
                self._print(zpl)
        
        if format_id.type == 'single':
            for rec in records:
                printed_labels = 0
                while printed_labels < copies:
                    zpl = format_id.compile(rec, count)
                    printed_labels += 1
                    count += 1
                    self._print(zpl)

            

class ZPLFormat(models.Model):
    _name = 'zpl.format'
    _description = "ZPL Format"

    name = fields.Char("Nome", required=True)
    type = fields.Selection([('single', 'One label per record'), ('multi', 'One label for all records')], string="Labels per Record", required=True, default="single")
    
    size_code = fields.Char("Label Type Code")
    fallback_formats = fields.Many2many('zpl.format', 'zpl_format_fallback_rel', 'preferred_id', 'fallback_id', string="Fallback Formats", )
   
    body = fields.Text('Corpo Formato', required=True, default="""
<t>
^FX Utilizzare il linguaggio ZPL per i formati
^FX Inserire campi forniti dai record con <t t-esc=""/>
^FX
</t>
""")

    variable_ids = fields.One2many('zpl.format.variable', 'format_id')

    def compile(self, records, count=0):
        qweb = self.env['ir.qweb']

        return qweb.render(etree.fromstring(self.body), values={'docs': records, 'doc': records[0], 'count': count, 'context_now': lambda: datetime.datetime.now()})

class ZPLVariable(models.Model):
    _name = 'zpl.format.variable'
    _description = "ZPL Format Variable"
    _rec_name = "key"

    format_id = fields.Many2one('zpl.format', required=True, ondelete="cascade")
    key             = fields.Char('Campo', required=True)
    

    field_type      = fields.Selection([('value', 'Valore'), ('reference', 'Riferimento')], required=True, default='value', string="Tipo Campo")
    default_value   = fields.Char('Valore di Default')

    @api.model
    def _selection_target_model(self):
        models = self.env['ir.model'].search([])
        return [(model.model, model.name) for model in models]
    
    ref_model   = fields.Many2one('ir.model', "Tabella di Riferimento")
    default_ref = fields.Reference(
        string='Record di Default', selection='_selection_target_model')

    @api.onchange('field_type')
    def _clear_reference_field(self):
        self.default_ref = False
        self.ref_model = ""
        self.default_value = ""