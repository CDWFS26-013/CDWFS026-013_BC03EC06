import sys
import time
import requests

BASE_URL = "http://localhost:5000"

def check(method, path, expected_status=200):
    url = f"{BASE_URL}{path}"
    resp = getattr(requests, method.lower())(url)
    if resp.status_code == expected_status:
        print(f"PASS [{method} {path}] -> {resp.status_code}: {resp.json()}")
        return True
    else:
        print(f"FAIL [{method} {path}] -> attendu {expected_status}, recu {resp.status_code}")
        print(f"  Reponse: {resp.text}")
        return False

print("Attente demarrage Flask...")
for i in range(15):
    try:
        requests.get(f"{BASE_URL}/water", timeout=1)
        print("App prete!")
        break
    except Exception:
        time.sleep(1)
else:
    print("ERREUR: L'app n'a pas demarre en 15 secondes")
    sys.exit(1)

results = []
results.append(check("GET",  "/water"))
results.append(check("PUT",  "/add_water"))
results.append(check("PUT",  "/add_water/user1"))
results.append(check("GET",  "/check_alert/user1"))

if not all(results):
    sys.exit(1)

print("\nTous les tests sont passes!")
