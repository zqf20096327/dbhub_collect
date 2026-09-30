# DM874-router
## Description
This service is responsible for sending messages to the correct websocket manager service (webserver).

It is also responsible for "bootstrapping" messages, since it contains a record that is dynamically adjustable of what services should handle a message.

## Interface
The service has two consumption topics, a topic for routing new messages through the message pipeline, and one for routing them back to the webserver (websocket manager).

The topics are specified in the `router-config` configmap.

## Configuration
This service is configured in the `application.conf` file which is in HOCON format (typesafe config).
