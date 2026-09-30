# Retrieval Authorization Boundary

A relevant document is not necessarily an authorized one. In retrieval-augmented generation, apply the caller's permissions before any passage is assembled into the model prompt. Derive identity from the application, propagate document or chunk ACLs into the index, and test revocation and cache behavior. A model instruction saying “ignore confidential passages” comes too late once the model has received the text.

Imagine a benefits query that matches a coworker's payroll record. Search ranking may place that record first. The permission filter must remove it, even though it is topically useful. After authorization, a separate relevance stage decides which allowed passages actually support the answer.

**Understanding check:** Why can an output filter not fully repair the mistake of giving the model an unauthorized payroll record?
