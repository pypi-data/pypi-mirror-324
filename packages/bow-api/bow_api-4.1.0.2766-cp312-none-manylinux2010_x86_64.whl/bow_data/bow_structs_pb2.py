# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bow_structs.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import bow_common_pb2 as bow__common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x62ow_structs.proto\x12\x0b\x62ow.structs\x1a\x10\x62ow_common.proto\"\xed\x02\n\x0b\x44\x61taMessage\x12\x34\n\tdata_type\x18\x01 \x01(\x0e\x32!.bow.structs.DataMessage.DataType\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x12\x11\n\ttimestamp\x18\x03 \x01(\x03\x12\x12\n\nRecordFlag\x18\x04 \x01(\x08\x12\x14\n\x0cPlaybackFlag\x18\x05 \x01(\x08\x12\x1a\n\x12PlaybackActionName\x18\x06 \x01(\t\"\xc0\x01\n\x08\x44\x61taType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\t\n\x05IMAGE\x10\x01\x12\t\n\x05\x41UDIO\x10\x02\x12\n\n\x06STRING\x10\x03\x12\x0e\n\nFLOAT32ARR\x10\x04\x12\x0c\n\x08INT64ARR\x10\x05\x12\x0b\n\x07\x43OMMAND\x10\x06\x12\t\n\x05MOTOR\x10\x07\x12\x08\n\x04\x42LOB\x10\x08\x12\x12\n\x0ePROPRIOCEPTION\x10\t\x12\x0b\n\x07TACTILE\x10\n\x12\x11\n\rINTEROCEPTION\x10\x0b\x12\x11\n\rEXTEROCEPTION\x10\x0c\"-\n\x07\x43ommand\x12\x0f\n\x07\x63ommand\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\"3\n\tDataArray\x12&\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x18.bow.structs.DataMessage\"\x81\x01\n\x08Location\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x10\n\x08hostname\x18\x02 \x01(\t\x12\x0c\n\x04\x63ity\x18\x03 \x01(\t\x12\x0e\n\x06region\x18\x04 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x05 \x01(\t\x12\x0b\n\x03loc\x18\x06 \x01(\t\x12\x0e\n\x06postal\x18\x07 \x01(\t\x12\x0b\n\x03org\x18\x08 \x01(\t\"{\n\rCalendarEntry\x12\x0f\n\x07robotID\x18\x01 \x01(\t\x12\x11\n\tunixStart\x18\x02 \x01(\x03\x12\x0f\n\x07unixEnd\x18\x03 \x01(\x03\x12\x12\n\nmodalities\x18\x04 \x03(\t\x12\x11\n\trecipient\x18\x05 \x01(\t\x12\x0e\n\x06issuer\x18\x06 \x01(\t\"\xb2\x01\n\x0b\x41udioParams\x12\x10\n\x08\x42\x61\x63kends\x18\x01 \x03(\t\x12\x12\n\nSampleRate\x18\x02 \x01(\r\x12\x10\n\x08\x43hannels\x18\x03 \x01(\r\x12\x14\n\x0cSizeInFrames\x18\x04 \x01(\x08\x12\x14\n\x0cTransmitRate\x18\x05 \x01(\r\x12\x17\n\x0f\x63\x61ptureModality\x18\x06 \x01(\t\x12\x14\n\x0csinkModality\x18\x07 \x01(\t\x12\x10\n\x08\x64\x65viceID\x18\x08 \x01(\t\"U\n\tGeoStruct\x12\x10\n\x08UpperLat\x18\x01 \x01(\x01\x12\x10\n\x08LowerLat\x18\x02 \x01(\x01\x12\x11\n\tUpperLong\x18\x03 \x01(\x01\x12\x11\n\tLowerLong\x18\x04 \x01(\x01\"M\n\x0c\x41ssetLicense\x12\x10\n\x08\x61sset_id\x18\x01 \x01(\t\x12+\n\rasset_license\x18\x02 \x01(\x0b\x32\x14.bow.structs.License\"\xc6\x01\n\x0cRobotLicense\x12\x10\n\x08robot_id\x18\x01 \x01(\t\x12\x10\n\x08\x61sset_id\x18\x02 \x01(\t\x12+\n\rrobot_license\x18\x03 \x01(\x0b\x32\x14.bow.structs.License\x12\x12\n\nrobot_make\x18\x04 \x01(\t\x12\x13\n\x0brobot_model\x18\x05 \x01(\t\x12\x11\n\tpair_code\x18\x06 \x01(\t\x12\x15\n\rpaired_status\x18\x07 \x01(\x08\x12\x12\n\nisFlexible\x18\x08 \x01(\x08\"\x82\x01\n\x07License\x12\x12\n\nlicense_id\x18\x01 \x01(\t\x12\x12\n\nstart_date\x18\x03 \x01(\x03\x12\x10\n\x08\x64uration\x18\x04 \x01(\x03\x12\x10\n\x08\x65nd_date\x18\x05 \x01(\x03\x12+\n\x08reseller\x18\x06 \x01(\x0b\x32\x19.bow.structs.ResellerInfo\"2\n\x05Share\x12\x17\n\x0frecipient_email\x18\x01 \x01(\t\x12\x10\n\x08\x64uration\x18\x02 \x01(\x03\"\x1d\n\nICEDetails\x12\x0f\n\x07\x64\x65tails\x18\x01 \x01(\t\"\xac\x01\n\x05\x41sset\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x05 \x01(\t\x12\x0f\n\x07license\x18\x06 \x01(\t\x12\x0c\n\x04make\x18\x07 \x01(\t\x12\r\n\x05model\x18\x08 \x01(\t\x12(\n\tartifacts\x18\t \x03(\x0b\x32\x15.bow.structs.Artifact\"\xbd\x01\n\x08\x41rtifact\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x10\n\x08\x61sset_id\x18\x02 \x01(\t\x12\n\n\x02OS\x18\x03 \x01(\t\x12\x0c\n\x04\x41rch\x18\x04 \x01(\t\x12\x14\n\x0cVersionMajor\x18\x05 \x01(\r\x12\x14\n\x0cVersionMinor\x18\x06 \x01(\r\x12\x14\n\x0cVersionPatch\x18\x07 \x01(\r\x12\x10\n\x08language\x18\x08 \x01(\t\x12\x11\n\ttimestamp\x18\t \x01(\x03\x12\x10\n\x08\x63hecksum\x18\n \x01(\x0c\"s\n\x0bPerformance\x12\x0c\n\x04Name\x18\x01 \x01(\t\x12\x13\n\x0b\x44\x65scription\x18\x02 \x01(\t\x12\x12\n\nAverageFPS\x18\x03 \x01(\x01\x12\x16\n\x0e\x41verageLatency\x18\x04 \x01(\x01\x12\x15\n\rFramesDropped\x18\x05 \x01(\x01\"{\n\x16PerformanceReportProto\x12?\n\x1drobotModalityPerformanceArray\x18\x01 \x03(\x0b\x32\x18.bow.structs.Performance\x12 \n\x05\x65rror\x18\x02 \x01(\x0b\x32\x11.bow.common.Error\"\x95\x01\n\x0cResellerInfo\x12\x16\n\x0e\x43ommissionName\x18\x01 \x01(\t\x12\x18\n\x10\x43ommissionRegion\x18\x02 \x01(\t\x12\x14\n\x0cResellerName\x18\x03 \x01(\t\x12\x16\n\x0eResellerRegion\x18\x04 \x01(\t\x12\x11\n\tIssueDate\x18\x05 \x01(\x03\x12\x12\n\nAssignedTo\x18\x06 \x01(\tBf\n\x0f\x63om.bow.structsB\x0f\x42owStructsProtoH\x01Z%github.com/Cyberselves/AnimusMessages\xa2\x02\nBowStructs\xaa\x02\x0b\x42OW.Structsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bow_structs_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017com.bow.structsB\017BowStructsProtoH\001Z%github.com/Cyberselves/AnimusMessages\242\002\nBowStructs\252\002\013BOW.Structs'
  _globals['_DATAMESSAGE']._serialized_start=53
  _globals['_DATAMESSAGE']._serialized_end=418
  _globals['_DATAMESSAGE_DATATYPE']._serialized_start=226
  _globals['_DATAMESSAGE_DATATYPE']._serialized_end=418
  _globals['_COMMAND']._serialized_start=420
  _globals['_COMMAND']._serialized_end=465
  _globals['_DATAARRAY']._serialized_start=467
  _globals['_DATAARRAY']._serialized_end=518
  _globals['_LOCATION']._serialized_start=521
  _globals['_LOCATION']._serialized_end=650
  _globals['_CALENDARENTRY']._serialized_start=652
  _globals['_CALENDARENTRY']._serialized_end=775
  _globals['_AUDIOPARAMS']._serialized_start=778
  _globals['_AUDIOPARAMS']._serialized_end=956
  _globals['_GEOSTRUCT']._serialized_start=958
  _globals['_GEOSTRUCT']._serialized_end=1043
  _globals['_ASSETLICENSE']._serialized_start=1045
  _globals['_ASSETLICENSE']._serialized_end=1122
  _globals['_ROBOTLICENSE']._serialized_start=1125
  _globals['_ROBOTLICENSE']._serialized_end=1323
  _globals['_LICENSE']._serialized_start=1326
  _globals['_LICENSE']._serialized_end=1456
  _globals['_SHARE']._serialized_start=1458
  _globals['_SHARE']._serialized_end=1508
  _globals['_ICEDETAILS']._serialized_start=1510
  _globals['_ICEDETAILS']._serialized_end=1539
  _globals['_ASSET']._serialized_start=1542
  _globals['_ASSET']._serialized_end=1714
  _globals['_ARTIFACT']._serialized_start=1717
  _globals['_ARTIFACT']._serialized_end=1906
  _globals['_PERFORMANCE']._serialized_start=1908
  _globals['_PERFORMANCE']._serialized_end=2023
  _globals['_PERFORMANCEREPORTPROTO']._serialized_start=2025
  _globals['_PERFORMANCEREPORTPROTO']._serialized_end=2148
  _globals['_RESELLERINFO']._serialized_start=2151
  _globals['_RESELLERINFO']._serialized_end=2300
# @@protoc_insertion_point(module_scope)
