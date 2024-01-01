import re

def extract_session_id(session_str: str):
    
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    
    if match:
        extracted_string = match.group(1)
        return extracted_string
    return ""


def get_str_from_expense_dict(expense_list: list):
    result_list = []

    for expense_dict in expense_list:
        result = []
        for key in ['category', 'amount', 'date']:
            if key in expense_dict:
                if key == 'date':
                    result.append(f"{key.capitalize()}: {expense_dict[key]}")
                elif key == 'category':
                    result.append(f"{key.capitalize()}: {expense_dict[key]}")
                else:
                    result.append(f"{key.capitalize()}: {float(expense_dict[key])}$")

        result_list.append(", ".join(result))

    return result_list

def get_str_from_budget_dict(budget_list: list):
    result_list = []

    for budget_dict in budget_list:
        result = []
        for key in ['category', 'amount', 'start_date', 'end_date']:
            if key in budget_dict:
                if key == 'start_date':
                    result.append(f"{key.capitalize()}: {budget_dict[key]}")
                elif key == 'end_date':
                    result.append(f"{key.capitalize()}: {budget_dict[key]}")
                elif key == 'category':
                    result.append(f"{key.capitalize()}: {budget_dict[key]}")
                else:
                    result.append(f"{key.capitalize()}: {float(budget_dict[key])}$")

        result_list.append(", ".join(result))

    return result_list