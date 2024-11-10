import re

import re
import sys

def extract_kv_from_string(s):
  pairs = re.findall(r'(\w+)=([^= ]+)', s)
  return {k: v for k, v in pairs}

# 读取并过滤数据
data = []
with open('/home/clay/timetrace.log', 'r') as file:

  block_number = 0
  start_time = 0
  prepare_time_started = 0
  prepare_time_ended = 0
  start_payload_started = 0
  start_payload_ended = 0
  get_payload_started = 0
  get_payload_ended = 0

  sanityCheckPayload_started = 0
  sanityCheckPayload_ended = 0
  PayloadToBlockRef_started = 0
  PayloadToBlockRef_ended = 0
  CommitUnsafePayload_started = 0
  CommitUnsafePayload_ended = 0

  PayloadProcessEvent_started = 0
  PayloadProcessEvent_ended = 0

  new_payload_started = 0
  new_payload_ended = 0
  fcu_started = 0
  fcu_ended = 0
  end = 0
  parent_number = 0

  for line in file:
    line = line.replace("\n", "")
    if not "MEGAETH" in line:
      continue
    kv = extract_kv_from_string(line)
    if "sql" not in kv:
      match(kv["step"]):
        case "start":
          tmp = start_time
          start_time = int(kv["time"])
          parent_number = int(kv["parent"])
          if block_number != 0:
            if parent_number != block_number:
              print(f"unexpected error:, {block_number}, {parent_number}")
              print(type(block_number))
              print(type(parent_number))

            sql = "insert into time_trace(block_number, start_time, interval0, prepare_time, interval1, start_payload, " \
            + "interval2, get_payload, interval3, new_payload, interval4, fcu, interval5, interval6, end, " \
            + "interval10, sanityCheckPayload, interval11, PayloadToBlockRef, interval12, CommitUnsafePayload, interval13, " \
            + "PayloadProcessEvent, " \
            + "metric)"
            # f"INSERT INTO {table_name} (name, age) VALUES ('{name}', {age});"
            # start_time, interval0
            sql = sql + f"values({block_number}, {tmp}, {prepare_time_started - tmp}, "
            # prepare_time
            sql = sql + f"{prepare_time_ended - prepare_time_started}, "
            # interval1
            sql = sql + f"{start_payload_started - prepare_time_ended},"
            # start_payload
            sql = sql + f"{start_payload_ended - start_payload_started}, "
            # interval2
            sql = sql + f"{get_payload_started - start_payload_ended}, "
            # get_payload
            sql = sql + f"{get_payload_ended - get_payload_started}, "
            # interval3
            sql = sql + f"{new_payload_started - get_payload_ended}, "
            # new_payload
            sql = sql + f"{new_payload_ended - new_payload_started}, "
            # interval4
            sql = sql + f"{fcu_started - new_payload_ended}, "
            # fcu
            sql = sql + f"{fcu_ended - fcu_started}, "
            # interval5
            sql = sql + f"{end - fcu_ended}, "
            # interval6
            sql = sql + f"{start_time - end}, "
            # end
            sql = sql + f"{end}, "

            #   sanityCheckPayload = 0
            #   PayloadToBlockRef = 0
            #   CommitUnsafePayload = 0
            # interval10
            sql = sql + f"{sanityCheckPayload_started - get_payload_ended}, "
            # sanityCheckPayload
            sql = sql + f"{sanityCheckPayload_ended - sanityCheckPayload_started}, "
            # interval11
            sql = sql + f"{PayloadToBlockRef_started - sanityCheckPayload_ended}, "
            # PayloadToBlockRef
            sql = sql + f"{PayloadToBlockRef_ended - PayloadToBlockRef_started}, "
            # interval12
            sql = sql + f"{CommitUnsafePayload_started - PayloadToBlockRef_ended}, "
            # CommitUnsafePayload
            sql = sql + f"{CommitUnsafePayload_ended - CommitUnsafePayload_started}, "
            # interval13
            sql = sql + f"{new_payload_started - CommitUnsafePayload_ended}, "
            # PayloadProcessEvent
            #sql = sql + f"{PayloadProcessEvent_ended - PayloadProcessEvent_started}, "
            sql = sql + f"{new_payload_started - PayloadProcessEvent_ended}, "

            sql = sql + f"'metric');\n"

            prepare_time_started = 0
            prepare_time_ended = 0
            start_payload_started = 0
            start_payload_ended = 0
            get_payload_started = 0
            get_payload_ended = 0
            new_payload_started = 0
            new_payload_ended = 0
            fcu_started = 0
            fcu_ended = 0
            end = 0
            block_number = 0
            with open("/home/clay/timetrace2.sql", "a") as file:
              file.write(sql)

        case "PreparePayloadAttributes_started":
          prepare_time_started = int(kv["time"])
        case "PreparePayloadAttributes_ended":
          prepare_time_ended = int(kv["time"])
        case "startPayload_started":
          start_payload_started = int(kv["time"])
        case "startPayload_ended":
          start_payload_ended = int(kv["time"])
        case "GetPayload_started":
          get_payload_started = int(kv["time"])
        case "GetPayload_ended":
          get_payload_ended = int(kv["time"])
        case "NewPayload_started":
          new_payload_started = int(kv["time"])
        case "NewPayload_ended":
          new_payload_ended = int(kv["time"])
        case "ForkchoiceUpdate_started":
          fcu_started = int(kv["time"])
        case "ForkchoiceUpdate_ended":
          fcu_ended = int(kv["time"])
        case "sanityCheckPayload_started":
          sanityCheckPayload_started = int(kv["time"])
        case "sanityCheckPayload_ended":
          sanityCheckPayload_ended = int(kv["time"])
        case "PayloadToBlockRef_started":
          PayloadToBlockRef_started = int(kv["time"])
        case "PayloadToBlockRef_ended":
          PayloadToBlockRef_ended = int(kv["time"])
        case "CommitUnsafePayload_started":
          CommitUnsafePayload_started = int(kv["time"])
        case "CommitUnsafePayload_ended":
          CommitUnsafePayload_ended = int(kv["time"])
        case "PayloadProcessEvent_started":
          PayloadProcessEvent_started = int(kv["time"])
        case "PayloadProcessEvent_ended":
          PayloadProcessEvent_ended = int(kv["time"])
        case "end":
          end = int(kv["time"])
          block_number = int(kv["currentBlock"])

