
import requests

def test_student_login():
    url = "http://127.0.0.1:5001/form_login/"
    data = {
        "username": "student1@test.com",
        "pass": "12345678"
    }
    
    session = requests.Session()
    response = session.post(url, data=data, allow_redirects=True)
    
    print(f"Status Code: {response.status_code}")
    print(f"Final URL: {response.url}")
    if "Incorrect Credentials" in response.text:
        print("Error: Incorrect Credentials")
    elif "Welcome" in response.text or "Dashboard" in response.text or "STUDENT ONE" in response.text:
        print("Success: Logged in as Student")
    else:
        print("Unknown response content.")
        # print(response.text[:500])

if __name__ == "__main__":
    test_student_login()
