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

from abc import ABC, abstractmethod
from typing import Optional, Union
from enum import IntEnum

from klat_connector.logger import LOG


class LoginState(IntEnum):
    DISCONNECTED = 0
    GUEST = 1
    USER = 2
    UNKNOWN = 3


class KlatApiABC(ABC):
    """Abstract class declaring the basic properties any inherited API should implement"""

    @property
    @abstractmethod
    def connected(self) -> bool:
        """
        Checks if instance is connected
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def nick(self) -> str:
        """
        Unique nickname for API instance in network
        """
        raise NotImplementedError

    @property
    def uid(self) -> str:
        """
        Override to specify a UID other than the login nick
        """
        return self.nick

    # Current Conversation properties
    @property
    def chat_log(self) -> Optional[list]:
        """
        Override to return a list of chat messages
        """
        return None

    @property
    def title(self) -> Optional[str]:
        """
        Override to return a conversation title
        """
        return None

    @property
    def logged_in(self) -> Union[int, LoginState]:
        """
        Override to return the login status of this instance
        """
        return LoginState.UNKNOWN

    @property
    def conversation_is_proctored(self) -> bool:
        """
        Override to return True if the conversation is proctored
        """
        return False

    @property
    def conversation_users(self) -> list:
        """
        Override to return a list of users in the current conversation
        """
        return []

    # Handlers to be overridden
    @abstractmethod
    def handle_incoming_shout(self, *args, **kwargs):
        """
        This function should be overridden to handle incoming messages
        """
        pass

    @abstractmethod
    def send_shout(self, shout: str, cid: str = None, dom: str = None,
                   **kwargs):
        """
        This method should be overridden to handle sending messages
        :param shout: text to shout
        :param cid: CID to send shout into (Private cid for @user shout)
        :param dom: Domain associated with cid
        """
        pass

    # Socket Listeners
    def _on_connect(self):
        """
        Handler for socket connection
        """
        LOG.info("Chat Server Socket Connected!")

    @staticmethod
    def _on_disconnect():
        """
        Handler for socket disconnection
        """
        # self.connected = False
        LOG.warning("Chat Server Socket Disconnected!")

    @staticmethod
    def _on_reconnect():
        """
        Handler for socket reconnection
        """
        # self.connected = True
        LOG.warning("SocketIO Reconnected")

    @abstractmethod
    def _on_user_message(self, *args):
        """
        Handler for "user message" (incoming shouts)
        :param args: Socket Arguments
        """
        pass

    @abstractmethod
    def _send_shout(self, *args, **kwargs):
        """
            Internal function that sends a shout into the conversation
        """
        pass

    @abstractmethod
    def _start_connection(self):
        """
        Initializes a new connection to the Klat server
        """
        pass

    @abstractmethod
    def _stop_connection(self):
        """
        Closes an open connection to the Klat server
        """
        pass

    @abstractmethod
    def _setup_listeners(self):
        """
        Starts all Klat event listeners
        """
        pass

    @abstractmethod
    def shutdown(self):
        """
        Clean up any pending transactions and close all connections.
        """

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Start any connections and perform any initialization that depends on
        connections. This may be called from `__init__`, or manually after
        object initialization.
        """
