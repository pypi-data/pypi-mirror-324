# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: generic_message.proto
# Protobuf Python Version: 5.29.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    3,
    '',
    'generic_message.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import config_message_pb2 as config__message__pb2
import data_message_pb2 as data__message__pb2
import otap_message_pb2 as otap__message__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15generic_message.proto\x12\x19wirepas.proto.gateway_api\x1a\x14\x63onfig_message.proto\x1a\x12\x64\x61ta_message.proto\x1a\x12otap_message.proto\"\x89\x0b\n\x0eWirepasMessage\x12<\n\x0cstatus_event\x18\x01 \x01(\x0b\x32&.wirepas.proto.gateway_api.StatusEvent\x12\x41\n\x0fget_configs_req\x18\x02 \x01(\x0b\x32(.wirepas.proto.gateway_api.GetConfigsReq\x12\x43\n\x10get_configs_resp\x18\x03 \x01(\x0b\x32).wirepas.proto.gateway_api.GetConfigsResp\x12?\n\x0eset_config_req\x18\x04 \x01(\x0b\x32\'.wirepas.proto.gateway_api.SetConfigReq\x12\x41\n\x0fset_config_resp\x18\x05 \x01(\x0b\x32(.wirepas.proto.gateway_api.SetConfigResp\x12\x41\n\x0fsend_packet_req\x18\x06 \x01(\x0b\x32(.wirepas.proto.gateway_api.SendPacketReq\x12\x43\n\x10send_packet_resp\x18\x07 \x01(\x0b\x32).wirepas.proto.gateway_api.SendPacketResp\x12M\n\x15packet_received_event\x18\x08 \x01(\x0b\x32..wirepas.proto.gateway_api.PacketReceivedEvent\x12T\n\x19get_scratchpad_status_req\x18\t \x01(\x0b\x32\x31.wirepas.proto.gateway_api.GetScratchpadStatusReq\x12V\n\x1aget_scratchpad_status_resp\x18\n \x01(\x0b\x32\x32.wirepas.proto.gateway_api.GetScratchpadStatusResp\x12M\n\x15upload_scratchpad_req\x18\x0b \x01(\x0b\x32..wirepas.proto.gateway_api.UploadScratchpadReq\x12O\n\x16upload_scratchpad_resp\x18\x0c \x01(\x0b\x32/.wirepas.proto.gateway_api.UploadScratchpadResp\x12O\n\x16process_scratchpad_req\x18\r \x01(\x0b\x32/.wirepas.proto.gateway_api.ProcessScratchpadReq\x12Q\n\x17process_scratchpad_resp\x18\x0e \x01(\x0b\x32\x30.wirepas.proto.gateway_api.ProcessScratchpadResp\x12\x45\n\x14get_gateway_info_req\x18\x0f \x01(\x0b\x32\'.wirepas.proto.gateway_api.GetGwInfoReq\x12G\n\x15get_gateway_info_resp\x18\x10 \x01(\x0b\x32(.wirepas.proto.gateway_api.GetGwInfoResp\x12h\n$set_scratchpad_target_and_action_req\x18\x11 \x01(\x0b\x32:.wirepas.proto.gateway_api.SetScratchpadTargetAndActionReq\x12j\n%set_scratchpad_target_and_action_resp\x18\x12 \x01(\x0b\x32;.wirepas.proto.gateway_api.SetScratchpadTargetAndActionResp\"(\n\x0f\x43ustomerMessage\x12\x15\n\rcustomer_name\x18\x01 \x02(\t\"\x8a\x01\n\x0eGenericMessage\x12:\n\x07wirepas\x18\x01 \x01(\x0b\x32).wirepas.proto.gateway_api.WirepasMessage\x12<\n\x08\x63ustomer\x18\x02 \x01(\x0b\x32*.wirepas.proto.gateway_api.CustomerMessage')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'generic_message_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_WIREPASMESSAGE']._serialized_start=115
  _globals['_WIREPASMESSAGE']._serialized_end=1532
  _globals['_CUSTOMERMESSAGE']._serialized_start=1534
  _globals['_CUSTOMERMESSAGE']._serialized_end=1574
  _globals['_GENERICMESSAGE']._serialized_start=1577
  _globals['_GENERICMESSAGE']._serialized_end=1715
# @@protoc_insertion_point(module_scope)
