# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2011 Zadara Storage Inc.
# Copyright (c) 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table
from sqlalchemy import Text, Boolean, ForeignKey

from nova import log as logging

meta = MetaData()

# Just for the ForeignKey and column creation to succeed, these are not the
# actual definitions of tables .
#

instances = Table('instances', meta,
       Column('id', Integer(),  primary_key=True, nullable=False),
       )

volumes = Table('volumes', meta,
       Column('id', Integer(),  primary_key=True, nullable=False),
       )

vsa_id = Column('vsa_id', Integer(), nullable=True)
to_vsa_id = Column('to_vsa_id', Integer(), nullable=True)
from_vsa_id = Column('from_vsa_id', Integer(), nullable=True)
drive_type_id = Column('drive_type_id', Integer(), nullable=True)


# New Tables
#

virtual_storage_arrays = Table('virtual_storage_arrays', meta,
       Column('created_at', DateTime(timezone=False)),
       Column('updated_at', DateTime(timezone=False)),
       Column('deleted_at', DateTime(timezone=False)),
       Column('deleted', Boolean(create_constraint=True, name=None)),
       Column('id', Integer(), primary_key=True, nullable=False),
       Column('display_name',
              String(length=255, convert_unicode=False, assert_unicode=None,
                     unicode_error=None, _warn_on_bytestring=False)),
       Column('display_description',
              String(length=255, convert_unicode=False, assert_unicode=None,
                     unicode_error=None, _warn_on_bytestring=False)),
       Column('project_id',
              String(length=255, convert_unicode=False, assert_unicode=None,
                     unicode_error=None, _warn_on_bytestring=False)),
       Column('availability_zone',
              String(length=255, convert_unicode=False, assert_unicode=None,
                     unicode_error=None, _warn_on_bytestring=False)),
       Column('instance_type_id', Integer(), nullable=False),
       Column('image_ref',
           String(length=255, convert_unicode=False, assert_unicode=None,
                  unicode_error=None, _warn_on_bytestring=False)),
       Column('vc_count', Integer(), nullable=False),
       Column('vol_count', Integer(), nullable=False),
       Column('status',
              String(length=255, convert_unicode=False, assert_unicode=None,
                     unicode_error=None, _warn_on_bytestring=False)),
       )

drive_types = Table('drive_types', meta,
       Column('created_at', DateTime(timezone=False)),
       Column('updated_at', DateTime(timezone=False)),
       Column('deleted_at', DateTime(timezone=False)),
       Column('deleted', Boolean(create_constraint=True, name=None)),
       Column('id', Integer(), primary_key=True, nullable=False),
       Column('name',
              String(length=255, convert_unicode=False, assert_unicode=None,
                     unicode_error=None, _warn_on_bytestring=False),
              unique=True),
       Column('type',
              String(length=255, convert_unicode=False, assert_unicode=None,
                     unicode_error=None, _warn_on_bytestring=False)),
       Column('size_gb', Integer(), nullable=False),
       Column('rpm',
              String(length=255, convert_unicode=False, assert_unicode=None,
                     unicode_error=None, _warn_on_bytestring=False)),
       Column('capabilities',
              String(length=255, convert_unicode=False, assert_unicode=None,
                     unicode_error=None, _warn_on_bytestring=False)),
       Column('visible', Boolean(create_constraint=True, name=None)),
       )

new_tables = (virtual_storage_arrays, drive_types)

#
# Tables to alter
#


def upgrade(migrate_engine):

    from nova import context
    from nova import db
    from nova import flags

    FLAGS = flags.FLAGS

    # Upgrade operations go here. Don't create your own engine;
    # bind migrate_engine to your metadata
    meta.bind = migrate_engine

    for table in new_tables:
        try:
            table.create()
        except Exception:
            logging.info(repr(table))
            logging.exception('Exception while creating table')
            raise

    instances.create_column(vsa_id)
    volumes.create_column(to_vsa_id)
    volumes.create_column(from_vsa_id)
    volumes.create_column(drive_type_id)


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    instances.drop_column(vsa_id)
    volumes.drop_column(to_vsa_id)
    volumes.drop_column(from_vsa_id)
    volumes.drop_column(drive_type_id)

    for table in new_tables:
        table.drop()
