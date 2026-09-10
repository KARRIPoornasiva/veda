import json
import sys
from http.cookiejar import CookieJar
from urllib import request, error

BASE_URL = "http://127.0.0.1:5000"


def fetch_json(path):
    url = BASE_URL + path
    try:
        with request.urlopen(url, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise AssertionError(f"HTTP error for {path}: {exc.code} - {body}") from exc
    except Exception as exc:  # pragma: no cover - test failure path
        raise AssertionError(f"Could not reach backend at {url}: {exc}") from exc


def admin_request(opener, path, method="GET", payload=None):
    url = BASE_URL + path
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with opener.open(req, timeout=5) as response:
            body = response.read().decode("utf-8", errors="replace")
            return response.status, json.loads(body) if body else {}
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body) if body else {}
        except json.JSONDecodeError:
            parsed = body
        raise AssertionError(f"HTTP error for {path}: {exc.code} - {parsed}") from exc


if __name__ == "__main__":
    try:
        status, health = fetch_json("/api/health")
        assert status == 200, f"health check status should be 200, got {status}"
        assert health.get("status") == "ok", health

        status, problems = fetch_json("/api/problems")
        assert status == 200, f"problems endpoint status should be 200, got {status}"
        assert isinstance(problems, list), problems
        assert len(problems) >= 1, "At least one problem should be returned"

        opener = request.build_opener(request.HTTPCookieProcessor(CookieJar()))
        login_status, login_body = admin_request(opener, "/api/admin/login", method="POST", payload={
            "username": "admin",
            "password": "veda-admin-2026",
        })
        assert login_status == 200, f"Admin login should succeed, got {login_status}: {login_body}"

        status, delete_body = admin_request(opener, "/api/admin/submissions", method="DELETE", payload={"all": True})
        assert status == 200, f"Delete submissions endpoint should return 200, got {status}: {delete_body}"
        assert isinstance(delete_body.get("deletedCount"), int), delete_body

        print("API smoke test passed.")
    except AssertionError as exc:
        print(f"TEST FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)


        # print("api tering tet passed")
        # status, problems = fetch_json("/api/problems")
        
    #     print("api smoke test passed.")
    # except AssertionError as exc:
    #     print(f"TEST FAILED: {exc}", file=sys.stderr)
    #     raise SystemExit(2)
        
    #     print("api unit testing passed.")
    # except AssertionError as exc:
    #     print(f"TEST FAILED: {exc}", file=sys.stderr)
    #     raise SystemExit(2)
    
    
    #     print("Test security test passed")
    # except AssertionError as exc:
    #     print(f"perforsnce testing")
        
        
        