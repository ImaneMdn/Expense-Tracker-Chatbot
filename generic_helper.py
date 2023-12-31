import re

def extract_session_id(session_str: str):
    
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    
    if match:
        extracted_string = match.group(1)
        return extracted_string
    return ""


def get_str_from_expense_dict(expense_dict: dict):
    result = []

    for key, value in expense_dict.items():
        if key == 'date':
            result.append(f"Date: {value}.")
        else:
            result.append(f"{int(value)}£ {key}, ")

    return ", ".join(result)