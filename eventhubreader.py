import logging
from azure.eventhub import EventHubConsumerClient

connection_str = 'Endpoint=sb://cpveventhub.servicebus.windows.net/;SharedAccessKeyName=cldr;SharedAccessKey=nfNSrQ576kJfh42BXN6IGjUh2SiEx3YzO/FbUZ7ERfI=;EntityPath=customercc'
consumer_group = '$Default'
eventhub_name = 'customercc'
client = EventHubConsumerClient.from_connection_string(connection_str, consumer_group, eventhub_name=eventhub_name)

logger = logging.getLogger("azure.eventhub")
logging.basicConfig(level=logging.INFO)

def on_event(partition_context, event):
    #logger.info("Received event from partition {}".format(partition_context.partition_id))
    print(event)
    partition_context.update_checkpoint(event)

with client:
    client.receive(
        on_event=on_event, 
        starting_position="-1",  # "-1" is from the beginning of the partition.
    )