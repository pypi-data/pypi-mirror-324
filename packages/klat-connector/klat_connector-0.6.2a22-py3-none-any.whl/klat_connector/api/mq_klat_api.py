# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
#
# Copyright 2008-2025 Neongecko.com Inc. | All Rights Reserved
#
# Notice of License - Duplicating this Notice of License near the start of any file containing
# a derivative of this software is a condition of license for this software.
# Friendly Licensing:
# No charge, open source royalty free use of the Neon AI software source and object is offered for
# educational users, noncommercial enthusiasts, Public Benefit Corporations (and LLCs) and
# Social Purpose Corporations (and LLCs). Developers can contact developers@neon.ai
# For commercial licensing, distribution of derivative works or redistribution please contact licenses@neon.ai
# Distributed on an "AS IS” basis without warranties or conditions of any kind, either express or implied.
# Trademarks of Neongecko: Neon AI(TM), Neon Assist (TM), Neon Communicator(TM), Klat(TM)
# Authors: Guy Daniels, Daniel McKnight, Regina Bloomstine, Elon Gasper, Richard Leeds
#
# Specialized conversational reconveyance options from Conversation Processing Intelligence Corp.
# US Patents 2008-2021: US7424516, US20140161250, US20140177813, US8638908, US8068604, US8553852, US10530923, US10530924
# China Patent: CN102017585  -  Europe Patent: EU2156652  -  Patents Pending

import time
from typing import Optional

from neon_mq_connector.utils.rabbit_utils import create_mq_callback
from pika.exchange_type import ExchangeType
from neon_utils import LOG
from neon_mq_connector import MQConnector

from klat_connector.api.klat_api_abc import KlatApiABC


class KlatAPIMQ(KlatApiABC, MQConnector):
    def __init__(self, config: Optional[dict], service_name: str, vhost: str):
        """
        Create an API connection to Klat via RabbitMQ
        :param config: MQ Config dict
            ``` JSON Template of configuration:

                     { "users": {"<service_name>": { "user": "<username>",
                                                     "password": "<password>" }
                                }
                       "server": "localhost",
                       "port": 5672
                     }
            ```
        :param service_name: name of service credentials to use
        :param vhost: RabbitMQ vhost to connect to
        """
        # TODO: Spec default vhost to connect to
        MQConnector.__init__(self, config, service_name)
        self.current_conversations = set()
        self.vhost = vhost
        self._connected = False

    @property
    def connected(self) -> bool:
        return self._connected

    @property
    def nick(self) -> str:
        # TODO: Support login to arbitrary Klat account
        return self.uid

    @property
    def uid(self) -> str:
        return self.service_name + '-' + self.service_id

    def handle_incoming_shout(self, message_data: dict):
        """Handles incoming shout for this user"""
        LOG.info(f'Received message data: {message_data}')

    @create_mq_callback()
    def _on_user_message(self, body: dict):
        if body.get('cid', None) in self.current_conversations and (body.get('is_broadcast', False)
                                                                    or body.get('receiver', None) == self.nick):
            self.handle_incoming_shout(body)

    def send_shout(self, shout: str, cid: str = None, dom: str = None,
                   queue_name: str = 'user_message',
                   exchange: Optional[str] = None,
                   broadcast: bool = False, context: dict = None,
                   **kwargs):
        """
        Shout into the current conversation or else passed dom/cid
        :param shout: text to shout
        :param cid: CID to send shout into (Private cid for @user shout)
        :param dom: Domain associated with cid
        :param queue_name: name of the response mq queue
        :param exchange: name of mq exchange
        :param broadcast: to broadcast shout (defaults to False)
        :param context: message context to pass along with response
        :param kwargs: additional params to include in message body
            `bot_type`: Optional string BotTypes for chatbots
            `conversation_state`: Optional string ConversationState for cid
            `responded_shout`: Optional string messageID to reply to
        """
        # TODO: Handle current cid or most recent cid for dom as default?
        if not cid:
            raise ValueError("cid not specified")

        if broadcast:
            # prohibits fanouts to default exchange for consistency
            exchange = exchange if exchange else queue_name  # handle ''
            queue_name = ''
            exchange_type = ExchangeType.fanout.value
        else:
            exchange_type = ExchangeType.direct.value

        message_body = {
            'nick': self.uid,
            'service_name': self.service_name,
            'cid': cid,
            'dom': dom,
            'shout': shout,
            'context': context or dict(),
            'time': str(time.time()),
            'is_broadcast': broadcast,
            **kwargs
        }

        self._send_shout(queue_name=queue_name,
                         exchange=exchange,
                         exchange_type=exchange_type,
                         message_body=message_body)

    def _send_shout(self, queue_name: str = '', message_body: dict = None,
                    exchange: str = '',
                    exchange_type: str = ExchangeType.direct.value) -> str:
        """
        Sends shout from current instance

        :param queue_name: MQ queue name for emit (optional for publish=True)
        :param message_body: dict with relevant message data
        :param exchange: MQ exchange name for emit
        :param exchange_type: type of exchange to use based on ExchangeType
            (direct, fanout, topic...)
        :returns generated shout id
        """
        if not message_body:
            message_body = {}
        with self.create_mq_connection(vhost=self.vhost) as mq_connection:
            if exchange_type == ExchangeType.fanout.value:
                message_id = self.publish_message(connection=mq_connection,
                                                  request_data=message_body,
                                                  exchange=exchange,
                                                  expiration=3000)
            else:
                message_id = self.emit_mq_message(connection=mq_connection,
                                                  queue=queue_name,
                                                  request_data=message_body,
                                                  exchange=exchange)
        return message_id

    def run(self, *args, **kwargs):
        self._setup_listeners()
        MQConnector.run(self, *args, **kwargs)
        self._on_connect()

    def _start_connection(self):
        self.run(run_sync=False)

    def _stop_connection(self):
        self._on_disconnect()
        self.stop()

    def _on_connect(self):
        self._send_shout('connection', {'nick': self.uid,
                                        'service_name': self.service_name,
                                        'time': time.time()},
                         exchange_type=ExchangeType.fanout.value)
        self._connected = True

    def _on_disconnect(self):
        self._send_shout('disconnection', {'nick': self.uid,
                                           'service_name': self.service_name,
                                           'time': time.time()},
                         exchange_type=ExchangeType.fanout.value)
        self._connected = False

    def _on_reconnect(self):
        self._stop_connection()
        self._start_connection()

    def _setup_listeners(self):
        self.register_consumer('user message', self.vhost, 'user_message',
                               self._on_user_message,
                               self.default_error_handler)
        self.register_consumer('user message broadcast', self.vhost, '',
                               self._on_user_message,
                               self.default_error_handler,
                               exchange="user_message",
                               exchange_type=ExchangeType.fanout.value)

    def shutdown(self):
        """
        Shutdown this connection; stop all consumers and close all connections
        """
        self._stop_connection()
