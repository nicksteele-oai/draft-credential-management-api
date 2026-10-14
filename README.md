# Agent Credential Management

An independent v0 discussion draft for provider-controlled credential use by
software agents. This draft starts from the September 22, 2026 Site version
and narrows its public interface to discovery, selection, protected use,
status, cancellation, and revocation.

Source and discussion: https://github.com/nicksteele-oai/draft-credential-management-api

The draft draws on the W3C Credential Management API's request model,
Web Authentication's security properties, and the OpenID AuthZEN
Authorization API's policy vocabulary. It does not define a complete wire
protocol, identity-claim format, or delegation mechanism.

It is not a W3C, FIDO Alliance, or OpenID Foundation deliverable.

## Build

```sh
make setup
make check
make preview
```

Open http://127.0.0.1:8765/ in a browser on the same machine as the preview
server. `PREVIEW_HOST` and `PREVIEW_PORT` can override the local binding.
`make watch` rebuilds the HTML when the source changes.

`index.bs` is authoritative; `index.html` is its generated rendering. The
Python environment stays in `.venv`. Building or previewing locally does not
publish a website. See [LICENSE](LICENSE) for the repository's license terms.

## Design constraints

- Credential managers own policy, enforcement, mediation, approval, and secrets.
- Agents express intent; they do not select their own approval or exposure policy.
- Task context is authenticated by a trusted runtime, not established by model assertions.
- Credential discovery is audience-, action-, task-, and authorization-scoped.
- Protected operations return results or opaque references, not durable secrets.
- Explicitly authorized shared-secret release remains a separate delivery path.
- Provisioning happens out of band or through provider-controlled setup during
  `get` or `use`; there are no public `create` or `store` methods.
- Delegation is deferred. Responses may carry agent information under provider
  policy and the underlying protocol, without creating delegated authority.
- Common security requirements apply to all methods and private integrations.
- MCP integration is an informative appendix, not a required public transport.
- Enterprise policy integration can map requests to AuthZEN subject, resource,
  action, and context evaluations.

## Repository layout

```text
index.bs                    Authoritative Bikeshed specification.
index.html                  Generated specification.
biblio.json                 Local references for W3C, FIDO, OpenID, and IETF documents.
examples/                   Illustrative request and provider-side policy data.
scripts/validate_examples.py  Executable consistency checks.
requirements.txt            Pinned Bikeshed dependency.
Makefile                    Reproducible build and verification commands.
```

The JSON examples are informative implementation sketches. Their trusted-context
and policy objects are not standardized v0 message schemas, and requester-supplied
purpose or context fields do not establish authority.
