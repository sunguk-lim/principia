# HTTP Request Media-Type Validation

## Meaning

A request's media type describes how its body is represented. An endpoint that promises JSON should accept the formats deliberately included in that contract, not silently reinterpret every body as JSON. Successful parsing proves that some bytes fit a parser; it does not establish that the caller used an allowed request format.

## Mechanism

In [[http]], `Content-Type` describes the request body. `Accept` instead expresses the client's preferences for the response. Parse a declared media type with the framework's maintained facilities, including supported parameters, rather than an arbitrary substring test. For requests with a body, enforce the permitted representation before parsing and before any state-changing operation. A missing media type needs an explicit endpoint policy. Bodyless requests do not need that header solely for this rule.

An unsupported representation normally receives status 415. Malformed data in a supported representation is a different failure. A syntactically valid document can still violate field types, business constraints or authorization. Keep those checks separate and bound the body size before expensive parsing. An attacker-provided header is not proof that its contents are trustworthy.

## One example

A fictional `/preferences` route accepts JSON objects. Request A sends a valid object with `application/json`; request B sends the same bytes as `text/plain`; request C declares JSON but sends malformed syntax. The endpoint may parse and then validate A, reject B as unsupported before parsing, and reject C as malformed. No request should update preferences until all relevant checks pass.

The distinction matters for browser security. Ordinary cross-origin forms can use simple media types such as text/plain. If an API accepts those and forcibly parses them as JSON, a boundary that expected preflighted JSON requests can disappear. JSON-only handling is still not a complete browser-origin or user-authorization policy: permissive CORS configuration and other authorized request paths must also be considered.

## Check your understanding

Can rejecting text/plain replace authentication? No. Media type controls representation, not the caller's identity or permitted effect. Test supported parameter variants, absent and unsupported types, malformed syntax and oversized bodies, observing that rejection precedes every sensitive side effect.
