import requests
import os
from colors import colors


class GPTExplainerClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path, email):
        try:
            with open(file_path, 'rb') as file:
                if email.isspace() or email == '':
                    response = requests.post(f"{self.base_url}/upload", files={'file': file})
                else:
                    response = requests.post(f"{self.base_url}/upload", files={'file': file, 'email': email})
                    
        except FileNotFoundError:
            return None
        return response.json()['uid']

    def status(self, uid):
        response = requests.get(f"{self.base_url}/status/{uid}")
        data = response.json()
        return Status(data['status'], data['filename'], data['timestamp'], data['explanation'])

    def status_by_email(self, email, filename):
        response = requests.get(f"{self.base_url}/file_by_mail/{email}::{filename}")
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




def console(client):
    colors.Purple('''
┌───────────────────────────────────────────┐
│     welcome to the pptxGPT client!        │
├───────────────────────────────────────────┤
│ You can type "help" at any point for help │
└───────────────────────────────────────────┘''')
    
    while True:
        colors.LightPurple("Enter Action: ", end='')
        action = input()

        if "status -m" in action.lower():
            colors.LightPurple("Enter email: ", end='')
            if not colors.off:
                print('\033[95m', end='')
            email = input()
            
            colors.LightPurple("Enter filename: ", end='')
            if not colors.off:
                print('\033[95m', end='')
            filename = input()
            
            status = client.status_by_email(email, filename)

            if status.is_done():
                colors.Clear(status.explanation)

            elif status.is_unknown_uid():
                colors.Red(f"unknown file (the user don't have file named {filename}): ")
            else:
                colors.Yellow(f"Status: {status.status}")


        elif "status" in action.lower():
            colors.LightPurple("Enter uid: ", end='')
            if not colors.off:
                print('\033[95m', end='')
            uid = input()

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
            colors.LightPurple("Enter email (optional): ", end='')
            email = input()

            uid = client.upload(file_path, email)
            if uid is None:
                colors.Red("FileNotFoundError: given bad path\n")
                continue
            
            colors.Green("Uploaded file, UID: ", end='')
            colors.Purple({uid})

        elif "help" in action.lower():
            colors.Purple('''commands:
    upload    # upload your file and get his uid
    status    # get status for upload with his uid (use 'status -m' if you forgot the uid)
    quit      # exit the client''')
            
        elif "quit" in action.lower():
            quit()
  

if __name__ == "__main__":
    URL = 'http://localhost:5000'
    print('\nYou Can View Colors In Some Terminals')
    is_colored = input('Use Colored Version (y/n): ')
    
    if is_colored == 'n':
        colors.off = True
        
    console(GPTExplainerClient(URL))




