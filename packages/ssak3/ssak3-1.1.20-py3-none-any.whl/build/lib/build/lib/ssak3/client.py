import yaml
from .query import *

# --------------------------------------------------------------------------------------------------------------
def getkv(_client, _config, _domain, _target, _name, _opt):
    query_domain = f'query_{_domain}_{_target}'
    # apify 서버에 적용. loaded_data 를 overwrite함
    store = _client.key_value_stores().get_or_create(name=_config)
    begintrx = _client.key_value_store(store["id"]).get_record(f'{query_domain}{SX_EXT_YAML}') or None
    if not begintrx:
        return get_prompt(_domain, _name, _opt)
    if begintrx and "value" in begintrx:
        rdata = yaml.load(begintrx["value"], Loader=yaml.FullLoader)
        result = next((item for item in rdata if item['name'] == _name), None)
        if result:
            if _opt == FIX:
                return fix_query(_name.strip(), result[QUERY].strip())
            return result[_opt].strip()
    return None

# eof