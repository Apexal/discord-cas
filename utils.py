import json
from typing import Dict

def generate_nickname(user: Dict, client: Dict) -> str:
    nickname = user['first_name'][:20] + ' ' + \
        user['last_name'][0] + " '" + str(user['graduation_year'])[2:]

    if client['is_rcs_id_in_nickname']:
        nickname += f' ({user["rcs_id"]})'
    
    return nickname
