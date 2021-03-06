# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2014 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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

{
    'name': 'Stock Picking Mass Action',
    'version': '8.0.1.0.0',
    'author': 'Camptocamp,GRAP,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/stock-logistics-workflow/',
    'license': 'AGPL-3',
    'category': 'Warehouse Management',
    'depends': [
        'stock_account',
    ],
    'data': [
        'wizard/mass_action_view.xml',
        'data/ir_cron.xml',
    ],
    'test': [
        'test/test_stock_picking_mass_action.yml',
    ],
}
