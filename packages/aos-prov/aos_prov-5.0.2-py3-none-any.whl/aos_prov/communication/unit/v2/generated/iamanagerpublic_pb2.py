# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: iamanager/v2/iamanagerpublic.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from aos_prov.communication.unit.v2.generated import (
    iamanagercommon_pb2 as iamanager_dot_v2_dot_iamanagercommon__pb2,
)
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
  name='iamanager/v2/iamanagerpublic.proto',
  package='iamanager.v2',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\"iamanager/v2/iamanagerpublic.proto\x12\x0ciamanager.v2\x1a\x1bgoogle/protobuf/empty.proto\x1a\"iamanager/v2/iamanagercommon.proto\"4\n\nSystemInfo\x12\x11\n\tsystem_id\x18\x01 \x01(\t\x12\x13\n\x0b\x62oard_model\x18\x02 \x01(\t\"\x1a\n\tCertTypes\x12\r\n\x05types\x18\x01 \x03(\t\">\n\x0eGetCertRequest\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0e\n\x06issuer\x18\x02 \x01(\x0c\x12\x0e\n\x06serial\x18\x03 \x01(\t\"B\n\x0fGetCertResponse\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x10\n\x08\x63\x65rt_url\x18\x02 \x01(\t\x12\x0f\n\x07key_url\x18\x03 \x01(\t\"B\n\x12PermissionsRequest\x12\x0e\n\x06secret\x18\x01 \x01(\t\x12\x1c\n\x14\x66unctional_server_id\x18\x02 \x01(\t\"Y\n\x13PermissionsResponse\x12\x12\n\nservice_id\x18\x01 \x01(\t\x12.\n\x0bpermissions\x18\x02 \x01(\x0b\x32\x19.iamanager.v2.Permissions\"\x1d\n\nAPIVersion\x12\x0f\n\x07version\x18\x01 \x01(\x04\x32\x87\x04\n\x10IAMPublicService\x12\x43\n\rGetSystemInfo\x12\x16.google.protobuf.Empty\x1a\x18.iamanager.v2.SystemInfo\"\x00\x12\x41\n\x0cGetCertTypes\x12\x16.google.protobuf.Empty\x1a\x17.iamanager.v2.CertTypes\"\x00\x12H\n\x07GetCert\x12\x1c.iamanager.v2.GetCertRequest\x1a\x1d.iamanager.v2.GetCertResponse\"\x00\x12W\n\x0eGetPermissions\x12 .iamanager.v2.PermissionsRequest\x1a!.iamanager.v2.PermissionsResponse\"\x00\x12\x39\n\x08GetUsers\x12\x16.google.protobuf.Empty\x1a\x13.iamanager.v2.Users\"\x00\x12H\n\x15SubscribeUsersChanged\x12\x16.google.protobuf.Empty\x1a\x13.iamanager.v2.Users\"\x00\x30\x01\x12\x43\n\rGetAPIVersion\x12\x16.google.protobuf.Empty\x1a\x18.iamanager.v2.APIVersion\"\x00\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,iamanager_dot_v2_dot_iamanagercommon__pb2.DESCRIPTOR,])




_SYSTEMINFO = _descriptor.Descriptor(
  name='SystemInfo',
  full_name='iamanager.v2.SystemInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='system_id', full_name='iamanager.v2.SystemInfo.system_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='board_model', full_name='iamanager.v2.SystemInfo.board_model', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=117,
  serialized_end=169,
)


_CERTTYPES = _descriptor.Descriptor(
  name='CertTypes',
  full_name='iamanager.v2.CertTypes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='types', full_name='iamanager.v2.CertTypes.types', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=171,
  serialized_end=197,
)


_GETCERTREQUEST = _descriptor.Descriptor(
  name='GetCertRequest',
  full_name='iamanager.v2.GetCertRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='iamanager.v2.GetCertRequest.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='issuer', full_name='iamanager.v2.GetCertRequest.issuer', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='serial', full_name='iamanager.v2.GetCertRequest.serial', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=199,
  serialized_end=261,
)


_GETCERTRESPONSE = _descriptor.Descriptor(
  name='GetCertResponse',
  full_name='iamanager.v2.GetCertResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='iamanager.v2.GetCertResponse.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cert_url', full_name='iamanager.v2.GetCertResponse.cert_url', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='key_url', full_name='iamanager.v2.GetCertResponse.key_url', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=263,
  serialized_end=329,
)


_PERMISSIONSREQUEST = _descriptor.Descriptor(
  name='PermissionsRequest',
  full_name='iamanager.v2.PermissionsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='secret', full_name='iamanager.v2.PermissionsRequest.secret', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='functional_server_id', full_name='iamanager.v2.PermissionsRequest.functional_server_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=331,
  serialized_end=397,
)


_PERMISSIONSRESPONSE = _descriptor.Descriptor(
  name='PermissionsResponse',
  full_name='iamanager.v2.PermissionsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='service_id', full_name='iamanager.v2.PermissionsResponse.service_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='permissions', full_name='iamanager.v2.PermissionsResponse.permissions', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=399,
  serialized_end=488,
)


_APIVERSION = _descriptor.Descriptor(
  name='APIVersion',
  full_name='iamanager.v2.APIVersion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='iamanager.v2.APIVersion.version', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=490,
  serialized_end=519,
)

_PERMISSIONSRESPONSE.fields_by_name['permissions'].message_type = iamanager_dot_v2_dot_iamanagercommon__pb2._PERMISSIONS
DESCRIPTOR.message_types_by_name['SystemInfo'] = _SYSTEMINFO
DESCRIPTOR.message_types_by_name['CertTypes'] = _CERTTYPES
DESCRIPTOR.message_types_by_name['GetCertRequest'] = _GETCERTREQUEST
DESCRIPTOR.message_types_by_name['GetCertResponse'] = _GETCERTRESPONSE
DESCRIPTOR.message_types_by_name['PermissionsRequest'] = _PERMISSIONSREQUEST
DESCRIPTOR.message_types_by_name['PermissionsResponse'] = _PERMISSIONSRESPONSE
DESCRIPTOR.message_types_by_name['APIVersion'] = _APIVERSION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SystemInfo = _reflection.GeneratedProtocolMessageType('SystemInfo', (_message.Message,), {
  'DESCRIPTOR' : _SYSTEMINFO,
  '__module__' : 'iamanager.v2.iamanagerpublic_pb2'
  # @@protoc_insertion_point(class_scope:iamanager.v2.SystemInfo)
  })
_sym_db.RegisterMessage(SystemInfo)

CertTypes = _reflection.GeneratedProtocolMessageType('CertTypes', (_message.Message,), {
  'DESCRIPTOR' : _CERTTYPES,
  '__module__' : 'iamanager.v2.iamanagerpublic_pb2'
  # @@protoc_insertion_point(class_scope:iamanager.v2.CertTypes)
  })
_sym_db.RegisterMessage(CertTypes)

GetCertRequest = _reflection.GeneratedProtocolMessageType('GetCertRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETCERTREQUEST,
  '__module__' : 'iamanager.v2.iamanagerpublic_pb2'
  # @@protoc_insertion_point(class_scope:iamanager.v2.GetCertRequest)
  })
_sym_db.RegisterMessage(GetCertRequest)

GetCertResponse = _reflection.GeneratedProtocolMessageType('GetCertResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETCERTRESPONSE,
  '__module__' : 'iamanager.v2.iamanagerpublic_pb2'
  # @@protoc_insertion_point(class_scope:iamanager.v2.GetCertResponse)
  })
_sym_db.RegisterMessage(GetCertResponse)

PermissionsRequest = _reflection.GeneratedProtocolMessageType('PermissionsRequest', (_message.Message,), {
  'DESCRIPTOR' : _PERMISSIONSREQUEST,
  '__module__' : 'iamanager.v2.iamanagerpublic_pb2'
  # @@protoc_insertion_point(class_scope:iamanager.v2.PermissionsRequest)
  })
_sym_db.RegisterMessage(PermissionsRequest)

PermissionsResponse = _reflection.GeneratedProtocolMessageType('PermissionsResponse', (_message.Message,), {
  'DESCRIPTOR' : _PERMISSIONSRESPONSE,
  '__module__' : 'iamanager.v2.iamanagerpublic_pb2'
  # @@protoc_insertion_point(class_scope:iamanager.v2.PermissionsResponse)
  })
_sym_db.RegisterMessage(PermissionsResponse)

APIVersion = _reflection.GeneratedProtocolMessageType('APIVersion', (_message.Message,), {
  'DESCRIPTOR' : _APIVERSION,
  '__module__' : 'iamanager.v2.iamanagerpublic_pb2'
  # @@protoc_insertion_point(class_scope:iamanager.v2.APIVersion)
  })
_sym_db.RegisterMessage(APIVersion)



_IAMPUBLICSERVICE = _descriptor.ServiceDescriptor(
  name='IAMPublicService',
  full_name='iamanager.v2.IAMPublicService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=522,
  serialized_end=1041,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetSystemInfo',
    full_name='iamanager.v2.IAMPublicService.GetSystemInfo',
    index=0,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_SYSTEMINFO,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetCertTypes',
    full_name='iamanager.v2.IAMPublicService.GetCertTypes',
    index=1,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_CERTTYPES,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetCert',
    full_name='iamanager.v2.IAMPublicService.GetCert',
    index=2,
    containing_service=None,
    input_type=_GETCERTREQUEST,
    output_type=_GETCERTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetPermissions',
    full_name='iamanager.v2.IAMPublicService.GetPermissions',
    index=3,
    containing_service=None,
    input_type=_PERMISSIONSREQUEST,
    output_type=_PERMISSIONSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetUsers',
    full_name='iamanager.v2.IAMPublicService.GetUsers',
    index=4,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=iamanager_dot_v2_dot_iamanagercommon__pb2._USERS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SubscribeUsersChanged',
    full_name='iamanager.v2.IAMPublicService.SubscribeUsersChanged',
    index=5,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=iamanager_dot_v2_dot_iamanagercommon__pb2._USERS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetAPIVersion',
    full_name='iamanager.v2.IAMPublicService.GetAPIVersion',
    index=6,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_APIVERSION,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_IAMPUBLICSERVICE)

DESCRIPTOR.services_by_name['IAMPublicService'] = _IAMPUBLICSERVICE

# @@protoc_insertion_point(module_scope)
