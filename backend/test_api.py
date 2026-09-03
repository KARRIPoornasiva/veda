import json
import sys
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


if __name__ == "__main__":
    try:
        status, health = fetch_json("/api/health")
        assert status == 200, f"health check status should be 200, got {status}"
        assert health.get("status") == "ok", health

        status, problems = fetch_json("/api/problems")
        assert status == 200, f"problems endpoint status should be 200, got {status}"
        assert isinstance(problems, list), problems
        assert len(problems) >= 1, "At least one problem should be returned"

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
        
        
        