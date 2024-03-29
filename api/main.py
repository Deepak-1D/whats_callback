from fastapi import FastAPI, Request, BackgroundTasks
from datetime import datetime
import requests
from mangum import Mangum


app = FastAPI()


def send_req(dict_data):
    #requests.post("http://sit.rigelsoft.com:8487/bot?verify_co=CPNrQTPdhwYTdCjGU6ub",json=dict_data )
    requests.post("https://7b7f-35-207-202-6.in.ngrok.io/bot?verify_co=CPNrQTPdhwYTdCjGU6ub",json=dict_data )
    


@app.get("/{id}")
async def callback(id: str, req: Request):
    reqs_params = dict(req.query_params)
    try:
        code = reqs_params["hub.challenge"]
    except:
        return {"error": "code not found"}
    return int(code)

@app.post("/{id}")
async def get_message(id:str, request: Request, bgtask:BackgroundTasks):
    print(request)
    first_response = await request.json()
    print(first_response)
    status = first_response["entry"][0]["changes"][0]["value"]
    print(len(status))
    if len(status) == 3:
        if status["statuses"][0]["status"] == "read":
            status_data= {"Type": "status", "status":status["statuses"][0]["status"] , "id":status["statuses"][0]["id"], "send_to":status["statuses"][0]["recipient_id"], "timestamp":repr(datetime.fromtimestamp(int(status["statuses"][0]["timestamp"])))}
            #insert_data = tbl_sms_log(sms_log_response=str(jsonable_encoder(first_response)), whatsapp_msg_id=status_data["id"], whatsapp_status=status_data["status"] )
        elif status["statuses"][0]["status"] == "failed":
            status_data= {"Type": "status", "status":status["statuses"][0]["status"] , "id":status["statuses"][0]["id"], "send_to":status["statuses"][0]["recipient_id"], "timestamp":repr(datetime.fromtimestamp(int(status["statuses"][0]["timestamp"])))}
            #insert_data = tbl_sms_log(sms_log_response=str(jsonable_encoder(first_response)), whatsapp_msg_id=status_data["id"], whatsapp_status=status_data["status"] )
        else:
            try:
                #print(first_response)
                status_data= {"Type": "status", "status":status["statuses"][0]["status"] , "id":status["statuses"][0]["id"], "send_to":status["statuses"][0]["recipient_id"], "message_type":status["statuses"][0]["conversation"]["origin"]["type"], "timestamp":repr(datetime.fromtimestamp(int(status["statuses"][0]["timestamp"])))}
                #insert_data = tbl_sms_log(sms_log_response=str(jsonable_encoder(first_response)), whatsapp_msg_id=status_data["id"], whatsapp_status=status_data["status"] )
            except:
                print("some")
        #try:
            #session.add(insert_data)
            #session.commit()
        #except:
            #session.rollback()    

    if len(status) == 4:
        print(first_response)
        if status["messages"][0]["type"] in ["image", "document", "video"]:
            media_type = status["messages"][0]["type"]
            recv_data = {"who_id":id, "Type": "media", "name":status["contacts"][0]["profile"]["name"], "in_number":status["messages"][0]["from"], "in_id":status["messages"][0]["id"], "content":status["messages"][0][media_type]}
            print(recv_data)
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
            
        bgtask.add_task(send_req, recv_data)
        return {"status":"scuess"}
        requests.post("https://edda-35-207-202-6.in.ngrok.io/bot?verify_co=CPNrQTPdhwYTdCjGU6ub",json=recv_data )
        
   
handler = Mangum(app=app)
