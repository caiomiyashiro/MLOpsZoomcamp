# after setting up Azure Events Hub (= AWS Kinesis) and Azure Functions (= AWS Lambda)
# pip3 install azure-eventhub

from azure.eventhub import EventHubProducerClient, EventData
import asyncio
import json

# eventhub_name = '<YOUR EVENT HUB INSTANCE NAME>'
# connection_str = '<YOUR EVENT HUBS NAMESPACE CONNECTION STRING>'
eventhub_name = 'first-event-hub'
connection_str = '<hub_sender_key>'

producer = EventHubProducerClient.from_connection_string(connection_str, eventhub_name=eventhub_name)

async def run():
    event_data_batch = producer.create_batch()
    data1 = {
        "PULocationID": "166",
        "DOLocationID":"143",
        "trip_distance": 10.0,
    }
    data2 = {
        "PULocationID": "166",
        "DOLocationID":"143",
        "trip_distance": 30.0,
    }
    event_data_batch.add(EventData(json.dumps(data1)))
    event_data_batch.add(EventData(json.dumps(data2)))
    
    send_batch_response = producer.send_batch(event_data_batch)
    if send_batch_response is not None:
        await send_batch_response
    producer_close_response = producer.close()
    if producer_close_response is not None:
        await producer_close_response

loop = asyncio.get_event_loop()
loop.run_until_complete(run())