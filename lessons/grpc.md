# gRPC: a typed call across a network

## Meaning

gRPC is a framework for calling a named method on another program. The call may look like a local method invocation, but the client and server communicate over a network. The service contract specifies which methods exist and what request and response messages they accept.

## Mechanism

The usual starting point is a `.proto` file. It declares a service method and Protocol Buffers message types. Code generation creates a client stub and a server interface. Your server implements the interface; your client calls the stub. The library serializes the request, carries it on an HTTP/2 stream, and returns a decoded response or a gRPC status.

There are four call shapes. A **unary** call exchanges one request and one response. **Server streaming** sends one request and receives many messages. **Client streaming** sends many messages and receives one response. **Bidirectional streaming** lets both sides send sequences independently. HTTP/2 multiplexing lets multiple calls share a connection.

## One example

Imagine a `GetUser(UserRequest) returns (UserReply)` method. The client passes `user_id = 42` to its generated stub. The stub encodes the request and sends it. The server decodes it, looks up the user, and replies. The client receives either the user data or an error status.

A deadline can stop waiting, but it cannot prove the server did not perform the lookup or another side effect. Retrying a write operation requires special care.

## Check your understanding

**Question:** Which component defines the operation, which usually encodes the message, and which carries concurrent calls?

**Answer:** The service contract defines the operation; Protocol Buffers usually encodes messages; HTTP/2 carries calls on streams.
