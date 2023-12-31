from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db
import generic_helper


app = FastAPI()

inprogress_expense = {}

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
        # 'Expense.remove - context: ongoing-expense': remove_expense,
        # 'expense.complete-context:ongoing-expense': complete_expense,
        
    }
    
    return intent_handler_dict[intent](parameters, session_id)
        

def add_expense(parameters: dict, session_id: str):
    category = parameters['category']
    amounts = [item["amount"] for item in parameters["amount"]]
    # Access the first element of the 'date-time' list and extract the date
    date = parameters['date-time'][0].split("T")[0]
    
    if len(category) != len(amounts):
        fulfillment_text = "Sorry i didn't understand. Can you please specify category and amount"
    else:
        expense_data = list(zip(category, amounts))
        expense_data.append(('date', date))  # Add the date to the list
        
        new_expense_dict = dict(expense_data)
        
        if session_id in inprogress_expense:
            current_expense_dict = inprogress_expense[session_id]
            current_expense_dict.update(new_expense_dict)
            inprogress_expense[session_id] = current_expense_dict
        else:
            
            inprogress_expense[session_id] = new_expense_dict
        
        expense_str = generic_helper.get_str_from_expense_dict(inprogress_expense[session_id])   
        fulfillment_text = f"Received {expense_str}  do you need anything else?"
    
    return JSONResponse(content={
            "fulfillmentText": fulfillment_text
    })
    
    # def add_expense(parameters: dict):
    # category = parameters['category']
    # amount = [am['amount'] for am in parameters['amount']]
    # date = parameters['date-time'].split("T")[0]
    # if len(category) != len(amount):
    #     fulfillment_text = "Sorry i didn't understand. Can you please specify category and amount"
    # else:
    #     fulfillment_text = f"Received {category} and {amount} at {date} in the backend"
    
    # return JSONResponse(content={
    #         "fulfillmentText": fulfillment_text
    # })