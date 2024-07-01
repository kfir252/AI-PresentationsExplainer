import requests
import os

class GPTExplainerClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path):
        with open(file_path, 'rb') as file:
            response = requests.post(f"{self.base_url}/upload", files={'file': file})

        return response.json()['uid']

    def status(self, uid):
        response = requests.get(f"{self.base_url}/status/{uid}")
        data = response.json()

        return Status(data['status'], data['filename'], data['timestamp'], data['explanation'])

class Status:
    def __init__(self, status, filename, timestamp, explanation):
        self.status = status
        self.filename = filename
        self.timestamp = timestamp
        self.explanation = explanation

    def is_done(self):
        return self.status == 'done'

    def is_unknown_uid(self):
        return self.status == 'unknown_uid'

def main(full_url: str):
    client = GPTExplainerClient(full_url)
    # input action(upload/status)
    while(True):
        action = input("Enter Action[status/upload/quit]: ")
        if "status" in action.lower():
            uid = input("Enter uid: ")
            status = client.status(uid)

            if status.is_done():
                print(f"Explanation: {status.explanation}")
            elif status.is_unknown_uid():
                print(f"unknown_uid: {uid}")
            else:
                print(f"Status: {status.status}")

        elif "upload" in action.lower():
            file_path = input("Enter file path: ")
            uid = client.upload(file_path)
            print(f"Uploaded file, UID: {uid}")

        elif "quit" in action.lower():
            print("Client.Quit")
            break

        else:
            print("Unknown command!")
        print('')

if __name__ == "__main__":
    main('http://localhost:5000')




