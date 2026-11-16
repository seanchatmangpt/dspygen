# Ngrok credential contract

DSPyGen keeps ngrok configuration in source control, but **credential material is not a source artifact**.

## Supported boundary

- `ngrok.yml` may describe tunnels, addresses, protocols, and public host names.
- The ngrok authentication token is supplied at runtime through `NGROK_AUTHTOKEN` or an external secret store.
- A concrete `authtoken:` value in any tracked `*ngrok*.yml` or `*ngrok*.yaml` file is refused by `scripts/verify_ngrok_credentials.py`.
- The verifier reports only path, line, and typed reason. It never prints the candidate credential value.

## Verification

```bash
python scripts/verify_ngrok_credentials.py
python -m unittest tests.security.test_ngrok_credential_hygiene -v
```

The `Ngrok Credential Hygiene` GitHub Actions workflow executes both checks when the credential boundary or its verifier changes.

## Incident boundary

Repository remediation can remove committed credential material and prevent recurrence. Credential invalidation itself occurs at the credential provider and cannot be inferred from repository state. If a token has ever been exposed, rotate/revoke it through the provider before treating that external credential as safe.
