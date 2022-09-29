from fastapi import FastAPI, Request
from datetime import date, datetime
from fastapi import FastAPI
import requests, os
from fastapi.encoders import jsonable_encoder


app = FastAPI()





@app.get("/services/whatsapp/callback/{id}")
def callback(id: str, req: Request):
    reqs_params = dict(req.query_params)
    try:
        code = reqs_params["hub.challenge"]
    except:
        return {"error": "code not found"}
    return int(code)

@app.post("/services/whatsapp/callback/{id}")
async def get_message(id:str, request: Request):
    print(id)
    first_response = await request.json()
    status = first_response["entry"][0]["changes"][0]["value"]
    if len(status) == 3:
        if status["statuses"][0]["status"] == "read":
            status_data= {"Type": "status", "status":status["statuses"][0]["status"] , "id":status["statuses"][0]["id"], "send_to":status["statuses"][0]["recipient_id"], "timestamp":repr(datetime.fromtimestamp(int(status["statuses"][0]["timestamp"])))}
            #insert_data = tbl_sms_log(sms_log_response=str(jsonable_encoder(first_response)), whatsapp_msg_id=status_data["id"], whatsapp_status=status_data["status"] )
        elif status["statuses"][0]["status"] == "failed":
            status_data= {"Type": "status", "status":status["statuses"][0]["status"] , "id":status["statuses"][0]["id"], "send_to":status["statuses"][0]["recipient_id"], "timestamp":repr(datetime.fromtimestamp(int(status["statuses"][0]["timestamp"])))}
            #insert_data = tbl_sms_log(sms_log_response=str(jsonable_encoder(first_response)), whatsapp_msg_id=status_data["id"], whatsapp_status=status_data["status"] )
        else:
            try:
                print(first_response)
                status_data= {"Type": "status", "status":status["statuses"][0]["status"] , "id":status["statuses"][0]["id"], "send_to":status["statuses"][0]["recipient_id"], "message_type":status["statuses"][0]["conversation"]["origin"]["type"], "timestamp":repr(datetime.fromtimestamp(int(status["statuses"][0]["timestamp"])))}
                #insert_data = tbl_sms_log(sms_log_response=str(jsonable_encoder(first_response)), whatsapp_msg_id=status_data["id"], whatsapp_status=status_data["status"] )
            except:
                pass
        #try:
            #session.add(insert_data)
            #session.commit()
        #except:
            #session.rollback()    

    if len(status) == 4:
        print(first_response)
        if status["messages"][0]["type"] == "text":
            recv_data = {"who_id":id , "Type":"message", "name":status["contacts"][0]["profile"]["name"], "in_number":status["messages"][0]["from"], "in_id":status["messages"][0]["id"], "message":{"body":status["messages"][0]["text"]["body"], "type": status["messages"][0]["type"]}}
        if (status["messages"][0]["type"] == "interactive") and (status["messages"][0]["interactive"]["type"]== "button_reply"):
            recv_data = {"who_id":id , "Type":"interactive_reply", "name":status["contacts"][0]["profile"]["name"], "in_number":status["messages"][0]["from"], "in_id":status["messages"][0]["id"], "message":{"id":status["messages"][0]["interactive"]["button_reply"]["id"], "name": status["messages"][0]["interactive"]["button_reply"]["title"] }}
        if (status["messages"][0]["type"] == "interactive") and (status["messages"][0]["interactive"]["type"]== "list_reply"):
             recv_data = {"who_id":id , "Type":"interactive_list", "name":status["contacts"][0]["profile"]["name"], "in_number":status["messages"][0]["from"], "in_id":status["messages"][0]["id"], "message":{"id":status["messages"][0]["interactive"]["list_reply"]["id"], "name": status["messages"][0]["interactive"]["list_reply"]["title"] }}
        #insert_data = tbl_sms_log(sms_log_response=str(jsonable_encoder(first_response)), whatsapp_msg_id=recv_data["in_id"], whatsapp_status="recived" )
        #try:
            #session.add(insert_data)
            #session.commit()
        #except:
            #session.rollback()
    
        
        requests.post("https://bfa5-35-207-202-6.in.ngrok.io/bot?verify_co=CPNrQTPdhwYTdCjGU6ub",json=recv_data )
        requests.post("https://492f-35-207-202-6.in.ngrok.io/bot?verify_co=CPNrQTPdhwYTdCjGU6ub",json=recv_data )
        
   
