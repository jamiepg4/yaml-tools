from functools import partial
import re
import sys
import logging
import flatdict
logger = logging.getLogger(__name__)

def resolve_yamls(yaml_templates):
    merged_yaml = _merge_dicts(reversed(yaml_templates))
    flattened = flatdict.FlatDict(merged_yaml, delimiter=".")
    keep_resolving = True
    loops = 0
    while keep_resolving and loops < len(flattened):
        loops += 1
        keep_resolving = False
        for key, value in flattened.items():
            keys_to_resolve = re.findall("\$\{(.*?)\}", str(value))
            if len(keys_to_resolve) > 0: keep_resolving = True
            resolved_keys = _resolve_key_substition(flattened, keys_to_resolve)
            for sub_key, resolved_key in resolved_keys:
                flattened[key] = flattened[key].replace(
                            "${%s}" % sub_key, str(resolved_key))
    return flattened

def _resolve_key_substition(flattened, keys_to_resolve):
    #this function returns array of tuples to replace strings later
    resolved_keys = []
    if len(keys_to_resolve) > 0:
        for key_default in keys_to_resolve:
            key_default_split = key_default.split(":")
            sub_key = key_default_split[0]
            default = key_default_split[1] if len(key_default_split) == 2 else sub_key
            resolved = flattened.get(sub_key, default)
            resolved_keys.append((key_default,resolved))
        return resolved_keys
    else:
        return resolved_keys

def _merge_dicts(dicts):
    result = {}
    for dictionary in dicts:
        result.update(dictionary)
    return result

# def _is_list_or_dict(val):
#     if val == None:
#         return False
#     return type(val) == dict or type(val) == list
