import requests
import os
from colors import colors


class GPTExplainerClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                response = requests.post(f"{self.base_url}/upload", files={'file': file})
        except FileNotFoundError:
            return None
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

def colored(client):
    while True:
        colors.LightPurple("Enter Action[status/upload/quit]: ", end='')
        action = input()

        if "status" in action.lower():
            colors.LightPurple("Enter uid: ", end='')
            uid = input('\033[95m')

            status = client.status(uid)

            if status.is_done():
                colors.Clear(status.explanation)

            elif status.is_unknown_uid():
                colors.Red(f"Unknown_uid: {uid}")
            else:
                colors.Yellow(f"Status: {status.status}")

        elif "upload" in action.lower():
            colors.LightPurple("Enter file path: ", end='')
            file_path = input()

            uid = client.upload(file_path)
            if uid is None:
                colors.Red("FileNotFoundError: given bad path\n")
                continue
            
            colors.Green("Uploaded file, UID: ", end='')
            colors.Purple({uid})

        elif "quit" in action.lower():
            colors.Green("Client.Quit")
            break

        else:
            colors.Red("Unknown command!")
        print()
        
def uncolored(client):
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
            if uid is None:
                colors.Red("FileNotFoundError: given bad path\n")
                continue
            
            print(f"Uploaded file, UID: {uid}")

        elif "quit" in action.lower():
            print("Client.Quit")
            break

        else:
            print("Unknown command!")
        print('')

def main(full_url: str):
    client = GPTExplainerClient(full_url)
    # input action(upload/status)
    print('You Can View Colors In Some Terminals')
    is_colored = input('Use Colored Version (y/n): ')
    
    if is_colored == 'y':
        colored(client)
    else:
        uncolored(client)
    


if __name__ == "__main__":
    main('http://localhost:5000')




