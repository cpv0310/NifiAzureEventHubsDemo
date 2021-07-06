import time
import os
import uuid
import datetime
import random
import json

from collections import OrderedDict
from faker import Faker
from datetime import timezone


locales = OrderedDict([
    ('en-US', 1),
])
fake = Faker(locales)

# Get the list of locales specified during instantiation
fake.locales

# Get the list of internal generators of this `Faker` instance
f=fake.factories


fake['en-US']

def newcustomer():
    customerorder={}

    customerorder["ordertime"]=time.time()*1000

    customerorder["name"]=fake.name()

    customerorder["address"]=fake.address()
    customerorder["creditcardprovider"]=fake.credit_card_provider()
    customerorder["creditcardnumber"]=fake.credit_card_number()
    customerorder["creditcardcc"]=fake.credit_card_security_code()
    customerorder["creditcardexpire"]=fake.credit_card_expire()
    customerorder["cost"]=float(random.randrange(325, 1043))/100
    return customerorder

from azure.eventhub import EventHubProducerClient, EventData

# This script simulates the production of events for 10 devices.
devices = []
for x in range(0, 10):
    devices.append(str(uuid.uuid4()))

# Create a producer client to produce and publish events to the event hub.
producer = EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://cpveventhub.servicebus.windows.net/;SharedAccessKeyName=cldr;SharedAccessKey=nfNSrQ576kJfh42BXN6IGjUh2SiEx3YzO/FbUZ7ERfI=;EntityPath=customercc", eventhub_name="customercc")

while True:
    event_data_batch = producer.create_batch() # Create a batch. You will add events to the batch later. 
    for dev in devices:
        # Create a dummy reading.
        reading = newcustomer()
        s = json.dumps(reading) # Convert the reading into a JSON string.
        event_data_batch.add(EventData(s)) # Add event data to the batch.
    producer.send_batch(event_data_batch) # Send the batch of events to the event hub.
    time.sleep(2)

# Close the producer.    
producer.close()