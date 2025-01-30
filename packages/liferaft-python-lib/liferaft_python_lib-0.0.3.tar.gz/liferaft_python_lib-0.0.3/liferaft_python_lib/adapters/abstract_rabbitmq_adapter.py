from time import sleep
from typing import Any
from typing import Union

import pika

from liferaft_python_lib.abcs.queue_adapter_abc import QueueAdapterABC
from liferaft_python_lib.logger import LOG


class RabbitMQAdapter(QueueAdapterABC):
    """A class to manage RabbitMQ queue operations."""

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        ssl_options: Union[pika.SSLOptions, None],
        queue_name: str,
        has_error_queue: bool = False,
        error_queue_name: str = None,
        has_dead_letter_queue: bool = False,
        dead_letter_queue_name: str = None,
        max_retries: int = 2,
        on_message_callback: Any = None,
        consumption_limit: int = -1,
        message_auto_ack: bool = False,
        message_prefetch_count: int = 0,
    ) -> None:
        """Initialize the RabbitMQAdapter with RabbitMQ connection parameters.

        Args:
            host (str): The RabbitMQ server hostname.
            port (int): The RabbitMQ server port number.
            username (str): The username for authentication.
            password (str): The password for authentication.
            ssl_options (Union[pika.SSLOptions, None]): SSL options for the connection.
            pipeline (Type[PipelineABC]): The pipeline to use for message processing.
            on_message_callback (Any, optional): The callback function to handle incoming messages. Defaults to None.

        Returns:
            None
        """

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssl_options = ssl_options
        self.connection = None
        self.channel = None
        self.on_message_callback = on_message_callback
        self.queue_name = queue_name
        self.has_error_queue = has_error_queue
        self.error_queue_name = error_queue_name
        self.has_dead_letter_queue = has_dead_letter_queue
        self.dead_letter_queue_name = dead_letter_queue_name
        self.max_retries = max_retries
        self.consumption_limit = consumption_limit
        self.consumed_messages = 0
        self.message_auto_ack = message_auto_ack
        self.message_prefetch_count = message_prefetch_count

    def connect(self) -> bool:
        """Establish a connection to the RabbitMQ server.

        Returns:
            bool: True if the connection is successful, False otherwise.

        Raises:
            pika.exceptions.AMQPError: If an error occurs while connecting to the RabbitMQ server.
        """
        try:
            self._attempt_connection()
            LOG.info(f"Connected to RabbitMQ server on {self.host}:{self.port}")
            return True
        except pika.exceptions.AMQPError as e:
            LOG.error(
                f"Initial connection attempt failed. Retrying with backoff... \n {e}"
            )
            retries = 0
            while retries < self.max_retries:
                retries += 1
                delay = min(2**retries, 32)
                LOG.info(
                    f"Retrying connection attempt {retries} after {delay} seconds..."
                )
                sleep(delay)
                try:
                    self.disconnect()
                    self._attempt_connection()
                    LOG.info(f"Connected to RabbitMQ server on {self.host}:{self.port}")
                    return True
                except pika.exceptions.AMQPError as e:
                    LOG.error(f"Connection attempt {retries} failed. \n {e}")
            # If we exhaust all retries, log and raise the final exception
            LOG.error(f"Failed to connect after {self.max_retries} retries.")
            raise pika.exceptions.AMQPError(
                f"Unable to connect to RabbitMQ server after {self.max_retries} retries."
            )

    def _attempt_connection(self) -> None:
        """Attempt to establish a connection to RabbitMQ."""
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host, port=self.port, credentials=credentials
        )
        parameters.ssl_options = self.ssl_options

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.queue_name, durable=True)
        if self.has_error_queue:
            self.channel.queue_declare(queue=self.error_queue_name, durable=True)
        if self.has_dead_letter_queue:
            self.channel.queue_declare(queue=self.dead_letter_queue_name, durable=True)

        self.channel.basic_qos(prefetch_count=self.message_prefetch_count)

    def consume(self) -> None:
        """Begin consuming messages from the RabbitMQ queue using the
        configured pipeline.

        Returns:
            None
        """
        try:
            LOG.info("Starting message consumption...")
            if self.consumption_limit == -1:
                self.channel.basic_consume(
                    queue=self.queue_name,
                    auto_ack=self.message_auto_ack,
                    on_message_callback=self.run,
                )
                self.channel.start_consuming()
            elif self.consumption_limit > 0:
                self._consume_with_limits()
            else:
                LOG.error(f"Invalid consumption limit: {self.consumption_limit}.")
        except Exception as e:
            LOG.error(f"Error consuming the message: {e}")
            self.disconnect()
            raise e

    def _consume_with_limits(self) -> None:
        """Begin consuming messages from the RabbitMQ queue using the
        configured pipeline with a message limit.

        Args:
            message_limit (int): The maximum number of messages to consume.

        Returns:
            None
        """
        try:
            while self.consumed_messages < self.consumption_limit:
                method_frame, properties, body = self.channel.basic_get(
                    queue=self.queue_name, auto_ack=self.message_auto_ack
                )
                if method_frame:
                    self.run(self.channel, method_frame, properties, body)
                    self.consumed_messages += 1
                else:
                    LOG.info("Heartbeat - No messages in queue.")
                    sleep(5)
            LOG.info(
                f"Consumed the maximum number of messages: {self.consumption_limit}"
            )
        except Exception as e:
            LOG.error(f"Error during limited consumption: {e}")
            raise e

    def run(self, channel: Any, method: Any, properties: Any, body: bytes) -> None:
        """Trigger the pipeline and handle retries if required.

        Args:
            channel (Any): The RabbitMQ channel.
            method (Any): Delivery information about the message.
            properties (Any): Message properties.
            body (bytes): The message body.

        Returns:
            None

        Raises:
            Any: Any exceptions that occur during message processing.
        """
        try:
            self.on_message_callback(body)
            if not self.message_auto_ack:
                channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            LOG.error(f"Error consuming the message: {e}")
            self._move_to_error_queue(channel, body)

    def _move_to_error_queue(self, channel: Any, body: bytes):
        """Helper function to move a message to the error queue."""
        if self.has_error_queue:
            channel.basic_publish(
                exchange="",
                routing_key=self.error_queue_name,
                body=body,
                properties=pika.BasicProperties(delivery_mode=2),
            )
            LOG.info(f"Message moved to error queue {self.error_queue_name}.")
        else:
            LOG.warning("Error queue is not configured")

    def dispatch(self, body: Any) -> None:
        """Dispatches the given data to the adapters queue.

        Args:
            data (Any): The data to be dispatched.

        Returns:
            None
        """
        retries = 0
        while retries < 3:
            try:
                if not self.connection or self.connection.is_closed:
                    LOG.debug(f"Reconnecting to {self.queue_name}")
                    self.connect()
                self.channel.basic_publish(
                    exchange="",
                    routing_key=self.queue_name,
                    body=body,
                    properties=pika.BasicProperties(delivery_mode=2),
                )
                break
            except Exception as e:
                retries += 1
                LOG.error(
                    f"Error dispatching data to the {self.queue_name} queue, retrying... : {e}"
                )
                sleep(0.5)
                if retries >= 3:
                    LOG.error(
                        f"Maximum retries for dispatch to the {self.queue_name} reached: {e}"
                    )
                    raise e

    def disconnect(self) -> bool:
        """Close the connection to the RabbitMQ server.

        Returns:
            bool: True if the disconnection is successful, False otherwise.

        Raises:
            pika.exceptions.AMQPError: If an error occurs while disconnecting from RabbitMQ.
            Exception: If any other unexpected error occurs during the disconnection process.
        """
        try:
            if self.channel:
                self.channel.stop_consuming()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                self.connection = None
                self.channel = None
                LOG.info(
                    f"Disconnected from RabbitMQ server on {self.host}:{self.port}"
                )
                return True
        except Exception as e:
            LOG.error(f"Error during disconnection: {e}")
            raise pika.exceptions.AMQPError(f"Error during disconnection: {e}")
