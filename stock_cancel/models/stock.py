# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2012 Andrea Cometa All Rights Reserved.
#                       www.andreacometa.it
#                       openerp@andreacometa.it
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#    Ported to new API by Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, models, exceptions, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _check_restrictions(self):
        # Restrictions before remove quants
        if self.returned_move_ids or self.split_from:
            raise exceptions.UserError(_('Action not allowed. Move splited / with returned moves.'))  # noqa


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def has_valuation_moves(self):
        self.ensure_one()
        account_moves = self.env['account.move'].search(
            [('ref', '=', self.name)])
        return bool(account_moves)

    def _check_restrictions(self):
        # Only allow with incoming operations
        # backorder_id in picking
        # returned_move_ids in stock.move
        # split_from in stock.move
        if not self.picking_type_id.code == 'incoming':
            raise exceptions.UserError(_('Allowed only with incoming operations.'))  # noqa
        if self.backorder_id:
            raise exceptions.UserError(_('Not Allowed, picking has backorder.'))  # noqa

    @api.multi
    def action_revert_done(self):
        for picking in self:
            picking._check_restrictions()
            if picking.has_valuation_moves():
                raise exceptions.UserError(
                    _('Picking %s has valuation moves: '
                        'remove them first.')
                    % (picking.name))
            if picking.invoice_id:
                raise exceptions.UserError(
                    _('Picking %s has invoices!') % (picking.name))
            picking.move_lines.write({'state': 'draft'})
            # remove quants done
            for move in picking.move_lines:
                move._check_restrictions()
                move.quant_ids.with_context(force_unlink=True).unlink()
            picking.state = 'draft'
            picking.action_confirm()
            picking.do_prepare_partial()
            picking.message_post(
                _("The picking has been re-opened and set to draft state"))
        return
