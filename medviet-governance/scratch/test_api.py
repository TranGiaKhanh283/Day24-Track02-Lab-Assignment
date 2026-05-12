import requests
import time

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    print(f"Connecting to {base_url}...")
    # Wait for server to start
    for _ in range(5):
        try:
            requests.get(f"{base_url}/health")
            print("Server is online.")
            break
        except:
            print("Waiting for server...")
            time.sleep(2)
    
    # Test cases
    test_cases = [
        # (token, endpoint, expected_status)
        ("token-alice", "/api/patients/raw", 200),
        ("token-bob",   "/api/patients/raw", 403),
        ("token-bob",   "/api/patients/anonymized", 200),
        ("token-carol", "/api/metrics/aggregated", 200),
        ("token-carol", "/api/patients/raw", 403),
        ("token-dave",  "/api/patients/raw", 403),
        ("token-dave",  "/api/patients/anonymized", 403),
        ("invalid",     "/api/patients/raw", 401),
    ]
    
    all_passed = True
    for token, endpoint, expected in test_cases:
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers)
            print(f"Testing {endpoint} with {token}: Expected {expected}, Got {response.status_code}")
            if response.status_code != expected:
                all_passed = False
        except Exception as e:
            print(f"Error testing {endpoint}: {e}")
            all_passed = False
    
    if all_passed:
        print("\nOK: ALL API RBAC TESTS PASSED!")
    else:
        print("\nFAIL: SOME API TESTS FAILED!")


if __name__ == "__main__":
    test_api()
