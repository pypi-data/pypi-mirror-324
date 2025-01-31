import hashlib
from .constants import *
from .utils import prompt_template_yaml

# opt 종류
QUERY = 'query'
ENGINE = 'engine'
FIX = 'fix'
PROMPT = 'prompt'
KEYWORDS = 'keywords'
DESCRIPTION = 'description'

# --------------------------------------------------------------------------------------------------------------
def get_prompt(_domain, _target, _name, _opt):
    query_domain = f'query_{_domain}_{_target}'
    datadict = prompt_template_yaml(query_domain)
    for entry in datadict:
        if entry.get('name') == _name:
            if _opt == FIX:
                return fix_query(_name.strip(), entry[QUERY].strip())
            return entry[_opt].strip()
    return None

# --------------------------------------------------------------------------------------------------------------
# domain 별로 이름은 유니크 해야 함
# 'Hello | World + 한글 - "Test"'
# --------------------------------------------------------------------------------------------------------------
def fix_query(_name, _query):
    combined_query = _name + _query
    hash_bytes = hashlib.sha256(combined_query.encode()).digest()
    out =  bytes(a ^ b ^ c ^ d for a, b, c, d in zip(hash_bytes[:8], hash_bytes[8:16], hash_bytes[16:24], hash_bytes[24:]))
    return out.hex()

# --------------------------------------------------------------------------------------------------------------
def get_config_path(_domain, _target, project=SX_PROJECT_BASE):
    basic_path = f'{project}-{_domain}'
    target_path = f'{basic_path}-{_target}'
    return f'{target_path}-{AF_CONFIG}'

# eof