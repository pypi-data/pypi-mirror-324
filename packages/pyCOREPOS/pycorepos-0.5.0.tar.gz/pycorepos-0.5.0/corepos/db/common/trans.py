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
Common schema for transaction data models
"""

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declared_attr


class TransactionDetailBase:
    """
    Base class for POS transaction detail models, shared by Office +
    Lane.
    """

    # register
    register_no = sa.Column(sa.Integer(), nullable=True)

    # txn
    trans_id = sa.Column(sa.Integer(), nullable=True)
    trans_no = sa.Column(sa.Integer(), nullable=True)
    trans_type = sa.Column(sa.String(length=1), nullable=True)
    trans_subtype = sa.Column(sa.String(length=2), nullable=True)
    trans_status = sa.Column(sa.String(length=1), nullable=True)

    # cashier
    emp_no = sa.Column(sa.Integer(), nullable=True)

    # customer
    card_no = sa.Column(sa.Integer(), nullable=True)
    memType = sa.Column(sa.Integer(), nullable=True)
    staff = sa.Column(sa.Boolean(), nullable=True)

    ##############################
    # remainder is "line item" ...
    ##############################

    upc = sa.Column(sa.String(length=13), nullable=True)

    department = sa.Column(sa.Integer(), nullable=True)

    description = sa.Column(sa.String(length=30), nullable=True)

    quantity = sa.Column(sa.Float(), nullable=True)

    scale = sa.Column(sa.Boolean(), nullable=True, default=False)

    cost = sa.Column(sa.Numeric(precision=10, scale=2), nullable=True)

    unitPrice = sa.Column(sa.Numeric(precision=10, scale=2), nullable=True)

    total = sa.Column(sa.Numeric(precision=10, scale=2), nullable=True)

    regPrice = sa.Column(sa.Numeric(precision=10, scale=2), nullable=True)

    tax = sa.Column(sa.SmallInteger(), nullable=True)

    foodstamp = sa.Column(sa.Boolean(), nullable=True)

    discount = sa.Column(sa.Numeric(precision=10, scale=2), nullable=True)

    memDiscount = sa.Column(sa.Numeric(precision=10, scale=2), nullable=True)

    discountable = sa.Column(sa.Boolean(), nullable=True)

    discounttype = sa.Column(sa.Integer(), nullable=True)

    voided = sa.Column(sa.Integer(), nullable=True)

    percentDiscount = sa.Column(sa.Integer(), nullable=True)

    ItemQtty = sa.Column(sa.Float(), nullable=True)

    volDiscType = sa.Column(sa.Integer(), nullable=True)

    volume = sa.Column(sa.Integer(), nullable=True)

    VolSpecial = sa.Column(sa.Numeric(precision=10, scale=2), nullable=True)

    mixMatch = sa.Column(sa.String(length=13), nullable=True)

    matched = sa.Column(sa.Boolean(), nullable=True)

    numflag = sa.Column(sa.Integer(), nullable=True, default=0)

    charflag = sa.Column(sa.String(length=2), nullable=True)

    def __str__(self):
        txnid = '-'.join([str(val) for val in [self.register_no,
                                               self.trans_no,
                                               self.trans_id]])
        return f"{txnid} {self.description or ''}"
