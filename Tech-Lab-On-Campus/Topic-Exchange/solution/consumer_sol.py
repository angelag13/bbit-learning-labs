# Copyright 2024 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pika
import os
import json


class mqConsumer:
    def __init__(self, binding_key, exchange_name: str, queue_name="") -> None:
        # Save parameters to class variables
        self.exchangeName = exchange_name
        # Call setupRMQConnection
        self.setupRMQConnection()
        pass

    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        connection = pika.BlockingConnection(parameters=con_params)
        
        # Establish Channel
        self.channel = connection.channel()

        # Create the exchange if not already present
        self.channel.exchange_declare(
            exchange=self.exchangeName, exchange_type="topic"
        )

        pass

    def bindQueueToExchange(self, queueName: str, topic: str) -> None:
        # Bind Binding Key to Queue on the exchange
        self.channel.queue_bind(
            queue= queueName,
            routing_key= "Routing Key",
            exchange="Exchange Name",
        )

        pass

    def createQueue(self, queueName: str) -> None:
        # Create Queue if not already present
        self.channel.queue_declare(queue=queueName)
            
        # Set-up Callback function for receiving messages
        self.channel.basic_consume(
            queueName, self.on_message_callback, auto_ack=False
        )
        pass

    def on_message_callback(self, channel, method_frame, header_frame, body):
        # De-Serialize JSON message object if Stock Object Sent
        message = json.loads(body)
        # Acknowledge And Print Message
        channel.basic_ack(method_frame.delivery_tag, False)

        pass

    def startConsuming(self) -> None:
        # Start consuming messages
        self.channel.start_consuming()
        pass
