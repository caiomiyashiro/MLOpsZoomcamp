# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(blueprint) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints

import logging
import azure.functions as func


blueprint = func.Blueprint()


@blueprint.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="myeventhub",
                               connection="FUNCTIONS_WORKER_RUNTIME") 
def eventhub_trigger(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))
