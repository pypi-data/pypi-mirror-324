# Klat API

The `Klat Connector` provides programmatic access to a Klat server.


## SocketIO Klat v1 API
The `api.sio_klat_api` module provides a connector that is compatible with a
Klat 1.0 SocketIO server. By default, this connector will initiate a connection
upon initialization and be ready for use.
> This connector is also compatible with the `MachKlatServer` available in this
> package.

## MQ Klat v2 API
The `api.mq_klat_api` module provides a connector compatible with a Pyklatchat
server via MQ. This connector will not complete a connection until the `run` 
method is called.
