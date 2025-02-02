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
Data model for CORE POS "lane_op" DB
"""

import sqlalchemy as sa
from sqlalchemy import orm

from corepos.db.common import op as common


Base = orm.declarative_base()


class Parameter(common.ParameterBase, Base):
    """
    Data model for ``parameters`` table.
    """
    __tablename__ = 'parameters'


class Employee(common.EmployeeBase, Base):
    """
    Data model for ``employees`` table.
    """
    __tablename__ = 'employees'


class Department(Base):
    """
    Represents a department within the organization.
    """
    __tablename__ = 'departments'

    number = sa.Column('dept_no', sa.SmallInteger(), nullable=False,
                       primary_key=True, autoincrement=False)

    name = sa.Column('dept_name', sa.String(length=30), nullable=True)

    tax = sa.Column('dept_tax', sa.Boolean(), nullable=True)

    food_stampable = sa.Column('dept_fs', sa.Boolean(), nullable=True)

    limit = sa.Column('dept_limit', sa.Float(), nullable=True)

    minimum = sa.Column('dept_minimum', sa.Float(), nullable=True)

    discount = sa.Column('dept_discount', sa.Boolean(), nullable=True)

    see_id = sa.Column('dept_see_id', sa.SmallInteger(), nullable=True)

    modified = sa.Column(sa.DateTime(), nullable=True)

    modified_by_id = sa.Column('modifiedby', sa.Integer(), nullable=True)

    margin = sa.Column(sa.Float(), nullable=False)

    sales_code = sa.Column('salesCode', sa.Integer(), nullable=False)

    member_only = sa.Column('memberOnly', sa.SmallInteger(), nullable=False)

    line_item_discount = sa.Column(sa.Boolean(), nullable=True)

    wicable = sa.Column('dept_wicable', sa.Boolean(), nullable=True)

    def __str__(self):
        return self.name or ""


class Product(common.ProductBase, Base):
    """
    Data model for ``products`` table.
    """
    __tablename__ = 'products'


class CustomerClassic(Base):
    """
    Represents a customer of the organization.

    https://github.com/CORE-POS/IS4C/blob/master/pos/is4c-nf/lib/models/op/CustdataModel.php
    """
    __tablename__ = 'custdata'
    # __table_args__ = (
    #     sa.ForeignKeyConstraint(['memType'], ['memtype.memtype']),
    # )

    id = sa.Column(sa.Integer(), nullable=False, primary_key=True, autoincrement=True)

    card_number = sa.Column('CardNo', sa.Integer(), nullable=True)

    person_number = sa.Column('personNum', sa.SmallInteger(), nullable=True)

    first_name = sa.Column('FirstName', sa.String(length=30), nullable=True)

    last_name = sa.Column('LastName', sa.String(length=30), nullable=True)

    cash_back = sa.Column('CashBack', sa.Numeric(precision=10, scale=2), nullable=True)

    balance = sa.Column('Balance', sa.Numeric(precision=10, scale=2), nullable=True)

    discount = sa.Column('Discount', sa.SmallInteger(), nullable=True)

    member_discount_limit = sa.Column('MemDiscountLimit', sa.Numeric(precision=10, scale=2), nullable=True)

    charge_limit = sa.Column('ChargeLimit', sa.Numeric(precision=10, scale=2), nullable=True)
    
    charge_ok = sa.Column('ChargeOk', sa.Boolean(), nullable=True, default=True)

    write_checks = sa.Column('WriteChecks', sa.Boolean(), nullable=True, default=True)

    store_coupons = sa.Column('StoreCoupons', sa.Boolean(), nullable=True, default=True)

    type = sa.Column('Type', sa.String(length=10), nullable=True, default='PC')

    member_type_id = sa.Column('memType', sa.SmallInteger(), nullable=True)
    # member_type = orm.relationship(
    #     MemberType,
    #     primaryjoin=MemberType.id == member_type_id,
    #     foreign_keys=[member_type_id],
    #     doc="""
    #     Reference to the :class:`MemberType` to which this member belongs.
    #     """)

    staff = sa.Column(sa.Boolean(), nullable=True, default=False)

    ssi = sa.Column('SSI', sa.Boolean(), nullable=True, default=False)

    purchases = sa.Column('Purchases', sa.Numeric(precision=10, scale=2), nullable=True, default=0)

    number_of_checks = sa.Column('NumberOfChecks', sa.SmallInteger(), nullable=True, default=0)

    member_coupons = sa.Column('memCoupons', sa.Integer(), nullable=True, default=1)

    blue_line = sa.Column('blueLine', sa.String(length=50), nullable=True)

    shown = sa.Column('Shown', sa.Boolean(), nullable=True, default=True)

    last_change = sa.Column('LastChange', sa.DateTime(), nullable=True)

    def __str__(self):
        return "{} {}".format(self.first_name or '', self.last_name or '').strip()


# TODO: deprecate / remove this
CustData = CustomerClassic
