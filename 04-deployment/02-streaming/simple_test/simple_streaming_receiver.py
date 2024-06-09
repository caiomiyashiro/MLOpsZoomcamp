# for consumer to checkpoint. aio is for async
# pip3 install azure-eventhub-checkpointstoreblob-aio azure-eventhub-checkpointstoreblob

import asyncio
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore

eventhub_name = 'first-event-hub'
consumer_group = '$Default'
receiver_connection_str = '<hub_receiver_key>'
# receivers need to store checkpoint points from streaming somewhere
storage_conn_str = '<blob_connection_string>'
blob_container_name = '<blob_name>'

async def on_event(partition_context, event):
    # Put your code here.
    print(f'Received event: {event.body_as_str()}')
    await partition_context.update_checkpoint(event)  # Or update_checkpoint every N events for better performance.

async def main():
    checkpoint_store = BlobCheckpointStore.from_connection_string(
        storage_conn_str,
        blob_container_name
    )
    client = EventHubConsumerClient.from_connection_string(
        receiver_connection_str,
        consumer_group,
        eventhub_name=eventhub_name,
        checkpoint_store=checkpoint_store,
    )

    async with client:
        await client.receive(on_event)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())