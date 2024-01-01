from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db
import generic_helper


app = FastAPI()

inprogress_expense = {}
inprogress_budget = {}

@app.post("/")
async def handle_request(request: Request):
    # retrieve the json data from the request
    payload = await request.json()
    
    # extract the necessary information from the payload
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    
    session_id = generic_helper.extract_session_id(output_contexts[0]['name'])
    
    intent_handler_dict = {
        'Expense.add - context: ongoing-expense': add_expense,
        'Expense.remove - context: ongoing-expense': remove_expense,
        'expense.complete-context:ongoing-expense': complete_expense,
        'SetBudget.add - context: ongoing-budget': set_budget,
        'SetBudget.complete-context:ongoing-expense': complete_budget,
        'SetBudget.remove-context:ongoing-expense': remove_budget,
        'QueryExpense': query_expense_handler,
        
    }
    
    return intent_handler_dict[intent](parameters, session_id)


def remove_expense(parameters: dict, session_id: str):
    if session_id not in inprogress_expense:
        return JSONResponse(content={
            "fulfillmentText": "I'm having trouble finding your expense. Sorry! Can you place a new expense please?"
        })

    current_expense = inprogress_expense[session_id]
    categories_to_remove = parameters.get("categories", [])

    removed_expense = []
    no_such_expense = []
    
    print(current_expense)
    print(categories_to_remove)
    
    for category in categories_to_remove:
        category_found = False
        for expense in current_expense:
            if expense['category'] == category:
                removed_expense.append(category)
                current_expense.remove(expense)
                category_found = True
                break

        if not category_found:
            no_such_expense.append(category)

    if removed_expense:
        print(removed_expense)
        fulfillment_text = f'Removed {removed_expense} from your expense list.'

    if no_such_expense:
        print(no_such_expense)
        fulfillment_text = f'Your expense does not have {no_such_expense}.'

    # Check if the current_expense list is empty
    if not current_expense:
        fulfillment_text += ' Your expense is empty!'

    else:
        expense_str = generic_helper.get_str_from_expense_dict(current_expense)
        fulfillment_text += f' Here is what is left in your new expense: {expense_str}'

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

    
     
def complete_expense(parameters: dict, session_id: str):
    if session_id not in inprogress_expense:
        fulfillment_text = "I'm having a trouble finding your expense. Sorry! Can you place a new expense please?"
    else:
        expense = inprogress_expense[session_id]
        expense_id = save_to_db(expense)
        
        if expense_id == -1:
            fulfillment_text = "Sorry, I couldn't process your new expense due to a backend error. " \
                "Please place a new expense again"
        else: 
            fulfillment_text = f"Awesome. I have placed your expense."
        
        del inprogress_expense[session_id]
            
    return JSONResponse(content={
            "fulfillmentText": fulfillment_text
    })

def save_to_db(expense:list): 
    next_expense_id = db.get_next_expense_id() 
    for expense_dict in expense:
        category = expense_dict["category"]
        amount = expense_dict["amount"]
        date = expense_dict["date"]
        rcode = db.insert_expense(
            next_expense_id,
            category,
            amount,
            date
        )
        if rcode == -1:
            return -1
    return next_expense_id

def add_expense(parameters: dict, session_id: str):
    category = parameters['category']
    amounts = [item["amount"] for item in parameters["amount"]]
    # Access the first element of the 'date-time' list and extract the date
    date = parameters['date-time'][0].split("T")[0]
    
    if len(category) != len(amounts):
        fulfillment_text = "Sorry i didn't understand. Can you please specify category and amount"
    else:
        new_expense_dict = {
            'category': category[0],
            'amount': amounts[0],
            'date': date
        }
        
        if session_id in inprogress_expense:
            inprogress_expense[session_id].append(new_expense_dict)
        else:
            inprogress_expense[session_id] = [new_expense_dict]

        expense_str = generic_helper.get_str_from_expense_dict(inprogress_expense[session_id])   
        if expense_str:
           expense_list_str = "\n".join(f"- {expense}" for expense in expense_str)
        fulfillment_text = f"Thank you for your expenses. You submitted the following:\n{expense_list_str}\nDo you need anything else?"
    
    return JSONResponse(content={
            "fulfillmentText": fulfillment_text
    })
    
    




def save_to_db_budget(budget:list):  
    next_budget_id = db.get_next_budget_id() 
    for expense_dict in budget:
        category = expense_dict["category"]
        amount = expense_dict["amount"]
        start_date = expense_dict["start_date"]
        end_date = expense_dict['end_date']
        rcode = db.insert_budget(
            next_budget_id,
            category,
            amount,
            start_date,
            end_date
        )
        if rcode == -1:
            return -1
    return next_budget_id

def set_budget(parameters: dict, session_id: str):
    category = parameters['category']
    amounts = parameters["budgetAmount"]["amount"]
    start_date = parameters["date"]["startDate"].split("T")[0]
    end_date = parameters["date"]["endDate"].split("T")[0]


    new_budget_dict = {
        'category': category,
        'amount': amounts,
        'start_date': start_date,
        'end_date': end_date
        }
        
    if session_id in inprogress_budget:
        inprogress_budget[session_id].append(new_budget_dict)
    else:
        inprogress_budget[session_id] = [new_budget_dict]

    budget_str = generic_helper.get_str_from_budget_dict(inprogress_budget[session_id])   
    if budget_str:
        budget_list_str = "\n".join(f"- {budget}" for budget in budget_str)
        fulfillment_text = f"Thank you for your budget. You submitted the following:\n{budget_list_str}\nDo you need anything else?"
    
    return JSONResponse(content={
            "fulfillmentText": fulfillment_text
    })
    
def complete_budget(parameters: dict, session_id: str):
    if session_id not in inprogress_budget:
        fulfillment_text = "I'm having a trouble finding your budget. Sorry! Can you set a new budget please?"
    else:
        budget = inprogress_budget[session_id]
        budget_id = save_to_db_budget(budget)
        
        if budget_id == -1:
            fulfillment_text = "Sorry, I couldn't process your new budget due to a backend error. " \
                "Please place a new budget again"
        else: 
            fulfillment_text = f"Awesome. I have placed your budget."
        
        del inprogress_budget[session_id]
            
    return JSONResponse(content={
            "fulfillmentText": fulfillment_text
    })
    
    
def remove_budget(parameters: dict, session_id: str):
    if session_id not in inprogress_budget:
        return JSONResponse(content={
            "fulfillmentText": "I'm having trouble finding your budget. Sorry! Can you place a new budget please?"
        })

    current_budget = inprogress_budget[session_id]
    categories_to_remove = parameters.get("categories", [])

    removed_budget = [budget for budget in current_budget if budget['category'] in categories_to_remove]
    current_budget = [budget for budget in current_budget if budget['category'] not in categories_to_remove]

    if removed_budget:
        removed_categories = ', '.join([budget['category'] for budget in removed_budget])
        fulfillment_text = f'Removed {removed_categories} from your budget list.'

    if not current_budget:
        fulfillment_text += ' Your budget is empty!'

    else:
        budget_str = generic_helper.get_str_from_budget_dict(current_budget)
        budget_str = ', '.join(budget_str)
        fulfillment_text += f' Here is what is left in your new budget: {budget_str}'

    inprogress_budget[session_id] = current_budget

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def query_expense_handler(parameters, session_id):
    category = parameters['category']
    date_parameters = parameters["date"]
    start_date = None
    end_date = None
    
    if date_parameters:
       start_date = parameters["date"]["startDate"].split("T")[0]
       end_date = parameters["date"]["endDate"].split("T")[0]
       total_spending = db.query_expense(category, date= None, start_date=start_date, end_date=end_date)
    else:
    # Call the query_expense function from db.py
       total_spending = db.query_expense(category, date= None, start_date= None, end_date= None)

    if total_spending is not None:
        if start_date and end_date:
            date_range_str = f" from {start_date} to {end_date}"
        else:
            date_range_str = ""

        fulfillment_text = f"Your total spending{' on ' + category if category else ''}{date_range_str} is {total_spending}$.\nDo you need anything else?"
    else:
        fulfillment_text = "Sorry, I couldn't retrieve the information at the moment."

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })
