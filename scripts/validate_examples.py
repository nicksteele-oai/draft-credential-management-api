"""Check the specification's examples and generated Bikeshed rendering."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"


def load(name: str) -> dict:
    path = EXAMPLES / name
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path.name} must contain a JSON object")
    return value


def main() -> None:
    request = load("credential-use-request.json")
    trusted = load("trusted-request-context.json")
    evaluation = load("authzen-evaluation.json")
    decision = load("authzen-decision.json")
    result = load("protected-result.json")

    task_id = request["taskId"]
    assert trusted["taskId"] == task_id, "trusted context must identify the same task"
    assert evaluation["context"]["task_id"] == task_id, "policy must evaluate the same task"
    assert evaluation["subject"]["id"] == trusted["agentId"], "subject must be authenticated"
    assert evaluation["resource"]["id"] == request["credentialId"], "credential mismatch"
    assert evaluation["action"]["name"] == f"credential:{request['operation']}"
    assert trusted["issuedAt"] < trusted["expiresAt"], "task attestation must expire"
    assert decision["decision"] is True, "success example requires an allow decision"
    assert decision["context"]["obligations"]["provider_retained"] is True
    assert result["response"]["status"] == 201, "result must be an HTTP response"

    forbidden_request_fields = {"mediation", "userVerification", "exposure", "policy"}
    for field in forbidden_request_fields:
        assert field not in request, f"requester must not control manager policy: {field}"

    forbidden_result_fields = {"secret", "privateKey", "accessToken", "refreshToken"}
    for field in forbidden_result_fields:
        assert field not in result, f"protected result must not disclose {field}"

    source = (ROOT / "index.bs").read_text(encoding="utf-8")
    interface = re.search(r"interface CredentialManager\s*\{(.*?)\};", source, re.S)
    assert interface is not None, "public interface is missing"
    methods = re.findall(r"Promise<[^\n]+?>\s+(\w+)\(", interface.group(1))
    assert methods == ["getInfo", "discover", "get", "use", "status", "cancel", "revoke"], (
        "v0 must retain the agreed seven-method interface"
    )
    assert "grantId" not in source, "delegation grant input is deferred beyond v0"
    assert "A credential-backed response may identify the acting agent" in source

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    required_sections = (
        "Trust provenance and task context",
        "Protected operation execution",
        "Authorized shared-key release",
        "Security requirements and considerations",
        "Provider authorization and protected interaction",
        "Privacy and user interaction",
        "Appendix A. MCP provider integration",
    )
    for section in required_sections:
        assert section in html, f"rendered specification missing section: {section}"

    assert "Independent Discussion Draft (v0)" in html
    assert "independent proposal for external discussion" in html
    assert "waived all copyright" not in html, "do not inject an unauthorized copyright waiver"
    assert "Open Web Foundation Agreement" not in html, "do not inject an unauthorized license"

    print("Validated 5 JSON examples, the 7-method v0 interface, 7 rendered sections, and independent draft status.")


if __name__ == "__main__":
    main()
