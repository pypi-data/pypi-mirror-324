# -*- coding: utf-8; -*-
################################################################################
#
#  pyCOREPOS -- Python Interface to CORE POS
#  Copyright © 2018-2025 Lance Edgar
#
#  This file is part of pyCOREPOS.
#
#  pyCOREPOS is free software: you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  pyCOREPOS is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  pyCOREPOS.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Common schema for operational data models
"""

import sqlalchemy as sa


class ParameterBase:
    """
    Base class for Parameter models, shared by Office + Lane.
    """
    store_id = sa.Column(sa.SmallInteger(), primary_key=True, nullable=False)

    lane_id = sa.Column(sa.SmallInteger(), primary_key=True, nullable=False)

    param_key = sa.Column(sa.String(length=100), primary_key=True, nullable=False)

    param_value = sa.Column(sa.String(length=255), nullable=True)

    is_array = sa.Column(sa.Boolean(), nullable=True)

    def __str__(self):
        return f"{self.store_id}-{self.lane_id} {self.param_key}"


class EmployeeBase:
    """
    Base class for Employee models, shared by Office + Lane.
    """
    number = sa.Column('emp_no', sa.SmallInteger(), nullable=False,
                       primary_key=True, autoincrement=False)

    cashier_password = sa.Column('CashierPassword', sa.String(length=50), nullable=True)

    admin_password = sa.Column('AdminPassword', sa.String(length=50), nullable=True)

    first_name = sa.Column('FirstName', sa.String(length=255), nullable=True)

    last_name = sa.Column('LastName', sa.String(length=255), nullable=True)

    job_title = sa.Column('JobTitle', sa.String(length=255), nullable=True)

    active = sa.Column('EmpActive', sa.Boolean(), nullable=True)

    frontend_security = sa.Column('frontendsecurity', sa.SmallInteger(), nullable=True)

    backend_security = sa.Column('backendsecurity', sa.SmallInteger(), nullable=True)

    birth_date = sa.Column('birthdate', sa.DateTime(), nullable=True)

    def __str__(self):
        return ' '.join([self.first_name or '', self.last_name or '']).strip()


class ProductBase:
    """
    Base class for Product models, shared by Office + Lane.
    """
    id = sa.Column(sa.Integer(), nullable=False, primary_key=True, autoincrement=True)

    upc = sa.Column(sa.String(length=13), nullable=True)

    description = sa.Column(sa.String(length=30), nullable=True)

    brand = sa.Column(sa.String(length=30), nullable=True)

    formatted_name = sa.Column(sa.String(length=30), nullable=True)

    normal_price = sa.Column(sa.Float(), nullable=True)

    price_method = sa.Column('pricemethod', sa.SmallInteger(), nullable=True)

    group_price = sa.Column('groupprice', sa.Float(), nullable=True)

    quantity = sa.Column(sa.SmallInteger(), nullable=True)

    special_price = sa.Column(sa.Float(), nullable=True)

    special_price_method = sa.Column('specialpricemethod', sa.SmallInteger(), nullable=True)

    special_group_price = sa.Column('specialgroupprice', sa.Float(), nullable=True)

    special_quantity = sa.Column('specialquantity', sa.SmallInteger(), nullable=True)

    special_limit = sa.Column(sa.SmallInteger(), nullable=True)

    start_date = sa.Column(sa.DateTime(), nullable=True)

    end_date = sa.Column(sa.DateTime(), nullable=True)

    department_number = sa.Column('department', sa.SmallInteger(), nullable=True)

    size = sa.Column(sa.String(length=9), nullable=True)

    tax_rate_id = sa.Column('tax', sa.SmallInteger(), nullable=True)

    foodstamp = sa.Column(sa.Boolean(), nullable=True)

    scale = sa.Column(sa.Boolean(), nullable=True)

    scale_price = sa.Column('scaleprice', sa.Float(), nullable=True)

    mix_match_code = sa.Column('mixmatchcode', sa.String(length=13), nullable=True)

    created = sa.Column(sa.DateTime(), nullable=True)

    modified = sa.Column(sa.DateTime(), nullable=True)

    tare_weight = sa.Column('tareweight', sa.Float(), nullable=True)

    discount = sa.Column(sa.SmallInteger(), nullable=True)

    discount_type = sa.Column('discounttype', sa.SmallInteger(), nullable=True)

    line_item_discountable = sa.Column(sa.Boolean(), nullable=True)

    unit_of_measure = sa.Column('unitofmeasure', sa.String(length=15), nullable=True)

    wicable = sa.Column(sa.SmallInteger(), nullable=True)

    quantity_enforced = sa.Column('qttyEnforced', sa.Boolean(), nullable=True)

    id_enforced = sa.Column('idEnforced', sa.SmallInteger(), nullable=True)

    cost = sa.Column(sa.Float(), nullable=True)

    special_cost = sa.Column(sa.Float(), nullable=True)

    received_cost = sa.Column(sa.Float(), nullable=True)

    in_use = sa.Column('inUse', sa.Boolean(), nullable=True)

    numflag = sa.Column(sa.Integer(), nullable=True)

    subdepartment_number = sa.Column('subdept', sa.SmallInteger(), nullable=True)

    deposit = sa.Column(sa.Float(), nullable=True)

    local = sa.Column(sa.Integer(), nullable=True, default=0)

    store_id = sa.Column(sa.SmallInteger(), nullable=True)

    default_vendor_id = sa.Column(sa.Integer(), nullable=True)

    current_origin_id = sa.Column(sa.Integer(), nullable=True)

    auto_par = sa.Column(sa.Float(), nullable=True, default=0)

    price_rule_id = sa.Column(sa.Integer(), nullable=True, default=0)

    last_sold = sa.Column(sa.DateTime(), nullable=True)
