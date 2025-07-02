from flask import Flask, request, jsonify
import pandas as pd
import logging
from datetime import datetime
import os

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Load the CSV file
df = pd.read_csv('data.csv')

def find_user(user_id, user_name):
    if not user_id or not user_name:
        return None
    user_data = df[(df['ID'] == user_id) & (df['Name'].str.lower() == user_name.lower())]
    return user_data if not user_data.empty else None

def get_user_from_session(req_json):
    session_info = req_json.get("sessionInfo", {})
    params = session_info.get("parameters", {})
    user_id = params.get("id_number")
    user_name = params.get("name")
    return user_id, user_name

@app.route("/authenticate", methods=["POST"])
def authenticate():
    req = request.get_json()
    logging.debug(f"Received request JSON: {req}")
    user_id = req.get('id_number')
    user_name = req.get('name')

    logging.debug(f"Tag: {tag}, ID: {user_id}, Name: {user_name}")

    user_data = find_user(user_id, user_name)

    if user_data is None:
        return jsonify({
            "user_found": False,
            "authenticated": = False,
            "message": "We couldn't find a matching record for the provided ID and name. Please re-enter your details."
        })

    return jsonify({
        "user_found": True,
        "received_ID_number": user_id,
        "received_name": user_name,
        "authenticated": True,
        "message": "User authenticated successfully."
        "sessionInfo": {
            "parameters": {
                "id_number": user_id,
                "name": user_name
            }
        }
    })

@app.route("/due_date", methods=["POST"])
def get_due_date():
    req = request.get_json()
    user_id, user_name = extract_session_user(req)
    user_data = find_user(user_id, user_name)

    if user_data is None or user_data.empty:
        return jsonify({"message": "User not authenticated."})
        
    due_date_str = user_data['Due Date'].values[0]
    due_date = datetime.strptime(due_date_str, "%m-%d-%Y").date()
    today = datetime.today().date()
    
    amount_due = user_data['Amount'].values[0]
    if due_date < today:
        message = "Your due date has passed."
        if amount_due > 0:
            message += " Along with your due amount, you have to pay extra 10 dollars as late fees."
        elif due_date == today:
            message = "Your due date is today."
        else:
            message = "Your due date is in the future."

        message += f" It is {due_date}."

        return jsonify({
            "due_date": str(due_date),
            "message": message
        })

@app.route("/amount_due", methods=["POST"])
def get_due_date():
    req = request.get_json()
    user_id, user_name = extract_session_user(req)
    user_data = find_user(user_id, user_name)

    if user_data is None or user_data.empty:
        return jsonify({"message": "User not authenticated."})
        
    amount_due = user_data['Amount'].values[0]
    message = f"The amount you have to pay is {amount_due}."
    return jsonify({
        "amount_due": float(amount_due),
        "message": message
    })

@app.route("/amount_due", methods=["POST"])
def get_due_date():
    req = request.get_json()
    user_id, user_name = extract_session_user(req)
    user_data = find_user(user_id, user_name)

    if user_data is None or user_data.empty:
        return jsonify({"message": "User not authenticated."})
        
    amount_due = user_data['Amount'].values[0]
    why_negative = user_data['Why Negative'].values[0]
    if amount_due < 0 and pd.notna(why_negative) and str(why_negative).strip():
        message = f"The reason for your negative balance is: {why_negative}. This amount will be adjusted in your next plan."
    else:
        message = "You do not have a negative balance."
    return jsonify({
        "why_negative": why_negative,
        "message": message
    })

@app.route("/amount_due", methods=["POST"])
def get_due_date():
    req = request.get_json()
    user_id, user_name = extract_session_user(req)
    user_data = find_user(user_id, user_name)

    if user_data is None or user_data.empty:
        return jsonify({"message": "User not authenticated."})
        
    plan_type = user_data['Plan'].values[0]
    message = f"Your plan type is {plan_type}."
    return jsonify({
        "plan_type": plan_type,
        "message": message
    })

    else:
    return jsonify({
        "message": "Unknown request type."
    })

    # except Exception as e:
    #     logging.exception("Webhook error:")
    #     return jsonify({
    #         "message": "An internal error occurred. Please try again later."
    #     }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)







# from flask import Flask, request, jsonify
# import pandas as pd
# import logging
# from datetime import datetime
# import os

# app = Flask(__name__)
# logging.basicConfig(level=logging.DEBUG)

# # Load the CSV file
# df = pd.read_csv('data.csv')

# def find_user(user_id, user_name):
#     if not user_id or not user_name:
#         return None
#     user_data = df[(df['ID'] == user_id) & (df['Name'].str.lower() == user_name.lower())]
#     return user_data if not user_data.empty else None

# @app.route("/webhook", methods=["POST"])
# def webhook():
#     try:
#         req = request.get_json()
#         logging.debug(f"Received request JSON: {req}")

#         tag = req.get('tag')
#         user_id = req.get('id_number')
#         user_name = req.get('name')

#         logging.debug(f"Tag: {tag}, ID: {user_id}, Name: {user_name}")

#         user_data = find_user(user_id, user_name)

#         if user_data is None:
#             return jsonify({
#                 "user_found": False,
#                 "received_ID_number": user_id,
#                 "received_name": user_name,
#                 "message": "We couldn't find a matching record for the provided ID and name. Please re-enter your details."
#             })

#         if tag == 'authenticate_user':
#             return jsonify({
#                 "user_found": True,
#                 "received_ID_number": user_id,
#                 "received_name": user_name,
#                 "authenticated": True,
#                 "message": "User authenticated successfully."
#             })

#         elif tag == 'get_due_date':
#             due_date_str = user_data['Due Date'].values[0]
#             due_date = datetime.strptime(due_date_str, "%m-%d-%Y").date()
#             today = datetime.today().date()
#             amount_due = user_data['Amount'].values[0]

#             if due_date < today:
#                 message = "Your due date has passed."
#                 if amount_due > 0:
#                     message += " Along with your due amount, you have to pay extra 10 dollars as late fees."
#             elif due_date == today:
#                 message = "Your due date is today."
#             else:
#                 message = "Your due date is in the future."

#             message += f" It is {due_date}."

#             return jsonify({
#                 "due_date": str(due_date),
#                 "message": message
#             })

#         elif tag == 'get_amount_due':
#             amount_due = user_data['Amount'].values[0]
#             message = f"The amount you have to pay is {amount_due}."
#             return jsonify({
#                 "amount_due": float(amount_due),
#                 "message": message
#             })

#         elif tag == 'get_negative_reason':
#             amount_due = user_data['Amount'].values[0]
#             why_negative = user_data['Why Negative'].values[0]
#             if amount_due < 0 and pd.notna(why_negative) and str(why_negative).strip():
#                 message = f"The reason for your negative balance is: {why_negative}. This amount will be adjusted in your next plan."
#             else:
#                 message = "You do not have a negative balance."
#             return jsonify({
#                 "why_negative": why_negative,
#                 "message": message
#             })

#         elif tag == 'get_plan_type':
#             plan_type = user_data['Plan'].values[0]
#             message = f"Your plan type is {plan_type}."
#             return jsonify({
#                 "plan_type": plan_type,
#                 "message": message
#             })

#         else:
#             return jsonify({
#                 "message": "Unknown request type."
#             })

#     except Exception as e:
#         logging.exception("Webhook error:")
#         return jsonify({
#             "message": "An internal error occurred. Please try again later."
#         }), 500

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)














# from flask import Flask, request, jsonify
# import pandas as pd
# import logging
# from datetime import datetime
# import os

# app = Flask(__name__)
# logging.basicConfig(level=logging.DEBUG)

# # Load the CSV file
# df = pd.read_csv('data.csv')

# def find_user(user_id, user_name):
#     if not user_id or not user_name:
#         return None
#     user_data = df[(df['ID'] == user_id) & (df['Name'].str.lower() == user_name.lower())]
#     return user_data if not user_data.empty else None

# @app.route("/webhook", methods=["POST"])
# def webhook():
#     try:
#         req = request.get_json()
#         logging.debug(f"Received request JSON: {req}")

#         tag = req.get('tag')
#         params = req
#         user_id = params.get('id_number')
#         user_name = params.get('name')

        
#         # tag = req.get('fulfillmentInfo', {}).get('tag')
#         # params = req.get('sessionInfo', {}).get('parameters', {})
#         # user_id = params.get('id_number')
#         # user_name = params.get('name')

#         logging.debug(f"Tag: {tag}, ID: {user_id}, Name: {user_name}")

#         user_data = find_user(user_id, user_name)

#         if user_data is None:
#             return jsonify({
#                 "fulfillment_response": {
#                     "messages": [
#                         {"text": {"text": ["We couldn't find a matching record for the provided ID and name. Please re-enter your details."]}}
#                     ]
#                 },
#                 "user_found": False,
#                         "received_ID_number": user_id,
#                         "received_name": user_name
#             })

#         if tag == 'authenticate_user':
#             return jsonify({
#                 "fulfillment_response": {
#                     "messages": [
#                         {"text": {"text": ["User authenticated successfully."]}}
#                     ]
#                 },
#                 "user_found": True,
#                         "received_ID_number": user_id,
#                         "received_name": user_name
#             })

#         elif tag == 'get_due_date':
#             due_date_str = user_data['Due Date'].values[0]
#             due_date = datetime.strptime(due_date_str, "%m-%d-%Y").date()
#             today = datetime.today().date()
#             amount_due = user_data['Amount'].values[0]

#             if due_date < today:
#                 message = "Your due date has passed. It was"
#                 if amount_due > 0:
#                     message += " Along with your due amount, you have to pay extra 10 dollars as late fees."
#             elif due_date == today:
#                 message = "Your due date is today. It is"
#             else:
#                 message = "Your due date is in the future. It is"

#             message += f" {due_date}."

#             return jsonify({
#                 "fulfillment_response": {
#                     "messages": [
#                         {"text": {"text": [message]}}
#                     ]
#                 },
#                 "due_date": str(due_date)
#             })

#         elif tag == 'get_amount_due':
#             amount_due = user_data['Amount'].values[0]
#             message = f"The amount you have to pay is {amount_due}."

#             return jsonify({
#                 "fulfillment_response": {
#                     "messages": [
#                         {"text": {"text": [message]}}
#                     ]
#                 },
#                 "amount_due": float(amount_due)
#             })

#         elif tag == 'get_negative_reason':
#             amount_due = user_data['Amount'].values[0]
#             why_negative = user_data['Why Negative'].values[0]
#             if amount_due < 0 and pd.notna(why_negative) and str(why_negative).strip():
#                 message = f"The reason for your negative balance is: {why_negative}. This amount will be adjusted in your next plan."
#             else:
#                 message = "You do not have a negative balance."
#             return jsonify({
#                 "fulfillment_response": {
#                     "messages": [
#                         {"text": {"text": [message]}}
#                     ]
#                 },
#                 "why_negative": why_negative
#             })

#         elif tag == 'get_plan_type':
#             plan_type = user_data['Plan'].values[0]
#             message = f"Your plan type is {plan_type}."
#             return jsonify({
#                 "fulfillment_response": {
#                     "messages": [
#                         {"text": {"text": [message]}}
#                     ]
#                 },
#                 "plan_type": plan_type
#             })

#         else:
#             return jsonify({
#                 "fulfillment_response": {
#                     "messages": [
#                         {"text": {"text": ["Unknown request type."]}}
#                     ]
#                 }
#             })

#     except Exception as e:
#         logging.exception("Webhook error:")
#         return jsonify({
#             "fulfillment_response": {
#                 "messages": [
#                     {"text": {"text": ["An internal error occurred. Please try again later."]}}
#                 ]
#             }
#         }), 500

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)






















# # from flask import Flask, request, jsonify
# # import pandas as pd
# # import logging
# # from datetime import datetime


# # app = Flask(__name__)
# # logging.basicConfig(level=logging.DEBUG)

# # # @app.route("/", methods=["GET", "HEAD"])
# # # def root():
# # #     return "", 204

# # # Load the CSV file
# # df = pd.read_csv('data.csv')

# # @app.route('/webhook', methods=['POST'])
# # def webhook():
# #     req = request.get_json(silent=True, force=True)
# #     logging.debug(f"Received request JSON: {req}")

# #     tag = req.get('fulfillmentInfo', {}).get('tag')
# #     params = req.get('sessionInfo', {}).get('parameters', {})
# #     user_id = params.get('id_number')
# #     user_name = params.get('name')

# #     logging.debug(f"Tag: {tag}, ID: {user_id}, Name: {user_name}")

# #     user_data = df[(df['ID'] == user_id) & (df['Name'].str.lower() == user_name.lower())]

# #     if user_data.empty:
# #         return jsonify({
# #             "fulfillment_response": {
# #                 "messages": [
# #                     {"text": {"text": ["We couldn't find a matching record for the provided ID and name. Please re-enter your details."]}}
# #                 ]
# #             },
# #             "session_info": {
# #                 "parameters": {
# #                     "user_found": False,
# #                     "received_ID_number": user_id,
# #                     "received_name": user_name
# #                 }
# #             }
# #         })

# #     else:
# #         # User is authenticated
# #         if tag == 'authenticate_user':
# #             return jsonify({
# #                 "fulfillment_response": {
# #                     "messages": [
# #                         {"text": {"text": ["User authenticated successfully. "]}}
# #                     ]
# #                 },
# #                 "session_info": {
# #                     "parameters": {
# #                         "user_found": True,
# #                         "received_ID_number": user_id,
# #                         "received_name": user_name
# #                     }
# #                 }
# #             })
    
# #         elif tag == 'get_due_date':
# #             due_date_str = user_data['Due Date'].values[0]
# #             due_date = datetime.strptime(due_date_str, "%m-%d-%Y").date()
# #             today = datetime.today().date()
# #             amount_due = user_data['Amount'].values[0]
# #             if due_date < today:
# #                 message = "Your due date has passed. It was " 
# #                 if amount_due > 0:
# #                     message += " Along with your due amount, you have to pay extra 10 dollars as late fees."
# #             elif due_date == today:
# #                 message = "Your due date is today. It is "
# #             else:
# #                 message = "Your due date is in the future. It is "

# #             message += f"{due_date}. "

# #             return jsonify({
# #                 "fulfillment_response": {
# #                     "messages": [
# #                         {"text": {"text": [message]}}
# #                     ]
# #                 },
# #                 "session_info": {
# #                     "parameters": {
# #                         "due_date": str(due_date)
# #                     }
# #                 }
# #             })
    
# #         elif tag == 'get_amount_due':
# #             amount_due = user_data['Amount'].values[0]
# #             message = f"The amount you have to pay is {amount_due}. "
    
# #             # if amount_due < 0:
# #             #     message += "To know why your balance is negative, please reply yes."
# #             # else:
# #             #     message += "Please reply yes to continue."
        
# #             return jsonify({
# #                 "fulfillment_response": {
# #                     "messages": [
# #                         {"text": {"text": [message]}}
# #                     ]
# #                 },
# #                 "session_info": {
# #                     "parameters": {
# #                         "amount_due": float(amount_due)
# #                     }
# #                 }
# #             })
    
    
# #         elif tag == 'get_negative_reason':
# #             amount_due = user_data['Amount'].values[0]
# #             why_negative = user_data['Why Negative'].values[0]
# #             if amount_due < 0 and pd.notna(why_negative) and str(why_negative).strip():
# #                 message = f"The reason for your negative balance is: {why_negative}. This amount will be adjusted in your next plan."
# #             else:
# #                 message = "You do not have a negative balance."
# #             return jsonify({
# #                 "fulfillment_response": {
# #                     "messages": [
# #                         {"text": {"text": [message]}}
# #                     ]
# #                 },
# #                 "session_info": {
# #                     "parameters": {
# #                         "why_negative": why_negative
# #                     }
# #                 }
# #             })
    
# #         elif tag == 'get_plan_type':
# #             amount_due = user_data['Amount'].values[0]
# #             plan_type = user_data['Plan'].values[0]
# #             message = f"Your plan type is {plan_type}. "
# #             # if amount_due != 0:
# #             #     message += "If you would like to make a payment, please reply pay."
# #             # else:
# #             #     message += "If you have any further questions, please reply yes."
# #             return jsonify({
# #                 "fulfillment_response": {
# #                     "messages": [
# #                         {"text": {"text": [message]}}
# #                     ]
# #                 },
# #                 "session_info": {
# #                     "parameters": {
# #                         "plan_type": plan_type
# #                     }
# #                 }
# #             })


# # if __name__ == '__main__':
# #     app.run(debug=True)

