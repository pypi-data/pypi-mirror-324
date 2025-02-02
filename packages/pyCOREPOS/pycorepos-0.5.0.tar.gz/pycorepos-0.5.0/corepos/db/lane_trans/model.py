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
Data model for CORE POS "lane_trans" DB
"""

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declared_attr

from corepos.db.common import trans as common


Base = orm.declarative_base()


class DTransactionBase(common.TransactionDetailBase):
    """
    Base class for ``dtransactions`` and similar models.
    """
    pos_row_id = sa.Column(sa.Integer(), primary_key=True, nullable=False)

    store_id = sa.Column(sa.Integer(), nullable=True, default=0)
    date_time = sa.Column('datetime', sa.DateTime(), nullable=True)


class DTransaction(DTransactionBase, Base):
    """
    Data model for ``dtransactions`` table.
    """
    __tablename__ = 'dtransactions'


class LocalTransBase(common.TransactionDetailBase):
    """
    Base class for ``localtrans`` and similar models.
    """

    @declared_attr
    def __table_args__(self):
        return (
            sa.PrimaryKeyConstraint('trans_id'),
        )

    date_time = sa.Column('datetime', sa.DateTime(), nullable=True)


class LocalTrans(LocalTransBase, Base):
    """
    Data model for ``localtrans`` table.
    """
    __tablename__ = 'localtrans'


class LocalTempTrans(LocalTransBase, Base):
    """
    Data model for ``localtemptrans`` table.
    """
    __tablename__ = 'localtemptrans'
