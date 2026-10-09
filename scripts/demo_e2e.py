#!/usr/bin/env python3
"""Run the complete A -> invite -> B -> relationship flow against Docker."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

BASE = os.getenv("API_BASE", "http://localhost/api/v1")

def call(path: str, method: str = "GET", payload: dict | None = None, token: str = "") -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=10) as response:
        body = json.loads(response.read())
        assert body["code"] == 0, body
        return body["data"]

def login(name: str) -> str:
    return call("/auth/wechat", "POST", {"mock_user": name})["access_token"]

def complete_test(token: str, invite_id: int | None = None) -> dict:
    test = call("/tests/hidden-personality", token=token)
    payload = {"test_slug": "hidden-personality"}
    if invite_id:
        payload["relation_invite_id"] = invite_id
    session = call("/test-sessions", "POST", payload, token)
    for index, question in enumerate(test["current_version"]["questions"]):
        option = question["options"][index % len(question["options"])]
        call(f"/test-sessions/{session['id']}/answers", "PUT", {"question_id": question["id"], "option_id": option["id"]}, token)
    return call(f"/test-sessions/{session['id']}/submit", "POST", {}, token)

def main() -> None:
    token_a = login("user_a")
    result_a = complete_test(token_a)["result_id"]
    call(f"/results/{result_a}/preview", token=token_a)
    call(f"/results/{result_a}/unlock", "POST", {"unlock_type": "MOCK"}, token_a)
    call(f"/results/{result_a}/full", token=token_a)
    invite = call("/relation-invites", "POST", {"result_id": result_a}, token_a)

    token_b = login("user_b")
    accepted = call(f"/relation-invites/{invite['invite_code']}/accept", "POST", {}, token_b)
    submitted_b = complete_test(token_b, accepted["invite_id"])
    relationship_id = submitted_b["relationship_id"]
    report = call(f"/relationships/{relationship_id}", token=token_b)
    assert 65 <= report["compatibility_score"] <= 95
    print(json.dumps({"status": "ok", "result_a": result_a, "relationship_id": relationship_id, "relation": report["report_payload"]["name"], "compatibility_score": report["compatibility_score"]}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
