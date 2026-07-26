---
id: http
title: HTTP
summary: "HTTP is the stateless request–response protocol of the web: a client opens a TCP connection to a server and sends a small text message (method + path + headers, optionally a body), and the server answers with a status code + headers + body — each exchange complete in itself."
type: concept
tags: [networking]
prereqs: [tcp, dns]
sources: [rfc-9110, "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview"]
status: explained
created: 2026-07-14
updated: 2026-07-14
---

# HTTP

## Summary

**HTTP** (HyperText Transfer Protocol) is the application protocol of the web. It is a
**request–response** protocol: a client sends one self-contained message asking a server to do
something to a named resource — "*GET* me `/index.html`", "*POST* this form to `/orders`" — and the
server sends back one self-contained answer: a numeric **status code** saying how it went, plus the
resource itself. Both messages are structured the same way: a first line, a list of `name: value`
**headers** (metadata), a blank line, and an optional **body**. HTTP itself carries no memory from
one exchange to the next — it is **stateless** — and it delegates all delivery work downward: the
bytes travel over a [[tcp]] connection, which guarantees they arrive complete and in order, so HTTP
never thinks about loss or reordering at all.

## Grounded explanation

### What it is — two message shapes over a reliable byte stream

[[tcp]] hands both ends a clean, reliable, ordered byte stream. HTTP is simply an agreement about
*what those bytes mean*: the client writes a **request**, the server writes a **response**, and each
has a fixed, readable shape (shown here in its classic text form, HTTP/1.1):

```
request                                  response
─────────────────────────────           ─────────────────────────────
GET /index.html HTTP/1.1                 HTTP/1.1 200 OK
Host: example.com                        Content-Type: text/html
Accept: text/html                        Content-Length: 1256
                                         
(no body for GET)                        <html> … 1256 bytes … </html>
```

- **Method** — the verb: what the client wants done. `GET` (read the resource), `POST` (submit data
  to it), `PUT` (replace it), `DELETE` (remove it), and a few others.
- **Path** — which resource on that server (`/index.html`).
- **Status code** — the server's three-digit verdict, grouped by first digit: `2xx` success
  (`200 OK`), `3xx` redirection ("it moved, look there"), `4xx` the *client's* mistake
  (`404 Not Found`, `403 Forbidden`), `5xx` the *server's* failure (`500 Internal Server Error`).
- **Headers** — open-ended `name: value` metadata on both sides: what formats the client accepts,
  what type and length the body is, caching rules, cookies, authentication tokens. Headers are
  HTTP's extension point: new features arrive as new headers, not new message shapes.
- **Body** — the payload proper: the HTML page, the JSON reply, the uploaded file.

### Why it works — statelessness, and the division of labor

**Why stateless.** Each request must carry *everything* the server needs to answer it (which
resource, credentials, accepted formats) — the protocol obliges the server to remember nothing
between requests. That is the key scaling insight: any of a thousand identical servers can answer
any request, a crashed server loses no protocol state, and a cache can answer a repeated `GET`
without involving the origin server at all. Where an application *does* need continuity (a login
session, a shopping cart), it layers it on top — the server hands the client a token in a header
(a cookie), and the client re-presents it on every request, keeping each exchange self-contained.

**Why over [[tcp]].** An HTTP message is only meaningful whole and in order — half a header list is
useless, and a body with a missing middle chunk is corrupt. [[tcp]] provides exactly that guarantee
(complete, ordered, duplicate-free bytes), so HTTP's design can be a *pure format*: no sequence
numbers, no retransmission, no acknowledgments of its own. One connection can then carry many
request–response exchanges back to back (**keep-alive**), saving the cost of a fresh connection
handshake per resource. (Newer wire versions keep the same request–response *semantics* — methods,
status codes, headers — while changing the encoding underneath: HTTP/2 multiplexes binary frames,
HTTP/3 moves off TCP entirely; and HTTPS is the same HTTP run through an encryption layer. Those
are wire-format evolution, incidental here.)

### Worked instance — one full GET, from name to page

A browser fetches `http://example.com/index.html`:

1. **Name → address.** The URL names the server by hostname, so the client first asks [[dns]] to
   resolve `example.com` → `93.184.216.34`.
2. **Connect.** The client opens a [[tcp]] connection to that address, port 80 (the HTTP default).
3. **Request.** It writes the request above — method `GET`, path `/index.html`, a `Host:` header
   (which of the possibly many sites at this address it means), and `Accept: text/html`.
4. **Respond.** The server locates the resource and writes back `HTTP/1.1 200 OK`, headers declaring
   `Content-Type: text/html` and `Content-Length: 1256`, a blank line, then exactly 1256 body bytes.
   The client knows precisely where the message ends because the header said so.
5. **Reuse or close.** With keep-alive, the same connection immediately carries the next request
   (the page's stylesheet, say); otherwise it closes.

The failure branches use the same shape, only the status line differs: a typo'd path gets
`404 Not Found` (a `4xx` — the client asked for something that isn't there); a crashing handler gets
`500 Internal Server Error` (a `5xx` — the server's own fault). The client code branches on the
first digit alone — that is what the grouping is for.

## Prerequisites

- [[tcp]] — the reliable, ordered byte stream every HTTP exchange rides on; HTTP is a pure message
  format because TCP already solved delivery
- [[dns]] — how the URL's hostname becomes the IP address the client actually connects to

## Sources

- RFC 9110 — HTTP Semantics (rfc-9110)
- MDN, "An overview of HTTP" — https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
