import os
import json
from datetime import datetime

# ANSIエスケープコード
BLUE = '\033[34m'
GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'

# グローバル変数
CURRENT_DIR = os.getcwd()
LOGGED_IN_USER = None
USERS_FILE = 'users.json'

def load_users():
    """ ユーザー情報をロードする """
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """ ユーザー情報を保存する """
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def add_user(user_id, password):
    """ ユーザーを追加する """
    users = load_users()
    if user_id in users:
        print("User already exists.")
    else:
        users[user_id] = password
        save_users(users)
        print(f"User '{user_id}' added successfully.")

def delete_user(user_id):
    """ ユーザーを削除する """
    users = load_users()
    if user_id in users:
        del users[user_id]
        save_users(users)
        print(f"User '{user_id}' deleted successfully.")
    else:
        print("User not found.")

def list_users():
    """ 現在のユーザーをリスト表示する """
    users = load_users()
    if users:
        print("Users:")
        for user in users.keys():
            print(f"- {user}")
    else:
        print("No users found.")

def login(user_id, password):
    """ ログイン処理 """
    global LOGGED_IN_USER
    users = load_users()
    if user_id in users and users[user_id] == password:
        LOGGED_IN_USER = user_id
        print(f"User '{user_id}' logged in.")
    else:
        print("Invalid credentials.")

def logout():
    """ ログアウト処理 """
    global LOGGED_IN_USER
    if LOGGED_IN_USER:
        print(f"User '{LOGGED_IN_USER}' logged out.")
        LOGGED_IN_USER = None
    else:
        print("No user is currently logged in.")

def whoami():
    """ 現在のログインユーザーを表示する """
    if LOGGED_IN_USER:
        print(f"Current logged in user: {LOGGED_IN_USER}")
    else:
        print("No user is currently logged in.")

def mkdir(dirname):
    """ ディレクトリを作成する """
    path = os.path.join(CURRENT_DIR, dirname)
    try:
        os.makedirs(path)
        print(f"Directory '{dirname}' created.")
    except FileExistsError:
        print(f"Directory '{dirname}' already exists.")

def cd(dirname):
    """ ディレクトリを移動する """
    global CURRENT_DIR
    path = os.path.join(CURRENT_DIR, dirname)
    if os.path.isdir(path):
        CURRENT_DIR = path
        print(f"Changed directory to '{CURRENT_DIR}'.")
    else:
        print(f"Directory '{dirname}' does not exist.")

def pwd():
    """ 現在の作業ディレクトリを表示する """
    print(CURRENT_DIR)

def ls():
    """ 現在のディレクトリ内のファイルとディレクトリをリスト表示する """
    try:
        for item in os.listdir(CURRENT_DIR):
            print(item)
    except FileNotFoundError:
        print("Directory not found.")

def rm(filename):
    """ ファイルを削除する """
    path = os.path.join(CURRENT_DIR, filename)
    if os.path.isfile(path):
        os.remove(path)
        print(f"File '{filename}' removed.")
    else:
        print(f"File '{filename}' does not exist.")

def mv(src, dest):
    """ ファイルを移動（名前変更）する """
    src_path = os.path.join(CURRENT_DIR, src)
    dest_path = os.path.join(CURRENT_DIR, dest)
    if os.path.isfile(src_path):
        os.rename(src_path, dest_path)
        print(f"File '{src}' renamed to '{dest}'.")
    else:
        print(f"File '{src}' does not exist.")

def wget(url):
    """ URL からファイルをダウンロードする (ダミー関数) """
    import requests
    try:
        response = requests.get(url)
        filename = url.split('/')[-1]
        with open(os.path.join(CURRENT_DIR, filename), 'wb') as file:
            file.write(response.content)
        print(f"Downloaded '{filename}'.")
    except Exception as e:
        print(f"Failed to download file: {e}")

def print_message(message):
    """ メッセージを表示する """
    print(message)

def display_time():
    """ 現在の時間を表示する """
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Current time: {formatted_time}")

def execute_command(command):
    """ コマンドを実行する関数 """
    parts = command.split(maxsplit=1)
    cmd = parts[0].lower()
    
    if cmd == "exit":
        print("Exiting the CLI OS...")
        return False
    elif cmd == "mkdir" and len(parts) == 2:
        mkdir(parts[1])
    elif cmd == "cd" and len(parts) == 2:
        cd(parts[1])
    elif cmd == "wget" and len(parts) == 2:
        wget(parts[1])
    elif cmd == "ls":
        ls()
    elif cmd == "pwd":
        pwd()
    elif cmd == "rm" and len(parts) == 2:
        rm(parts[1])
    elif cmd == "mv" and len(parts) == 3:
        mv(parts[1], parts[2])
    elif cmd == "adduser" and len(parts) == 2:
        add_user(parts[1], input("Enter password: "))
    elif cmd == "deluser" and len(parts) == 2:
        delete_user(parts[1])
    elif cmd == "listusers":
        list_users()
    elif cmd == "login" and len(parts) == 2:
        login(parts[1], input("Enter password: "))
    elif cmd == "logout":
        logout()
    elif cmd == "whoami":
        whoami()
    elif cmd == "print" and len(parts) == 2:
        print_message(parts[1])
    elif cmd == "time":
        display_time()
    else:
        print(f"Command '{cmd}' not recognized or invalid arguments.")
    
    return True

def main():
    """ メイン関数 """
    print("Welcome to CLI OS. Type 'exit' to quit.")
    while True:
        # プロンプトを表示
        user_id = LOGGED_IN_USER if LOGGED_IN_USER else 'guest'
        colored_path = f"{BLUE}{CURRENT_DIR}{RESET}"
        colored_user_id = f"{GREEN}{user_id}{RESET}"
        colored_arrow = f"{RED}➔{RESET}"
        prompt = f"@{colored_user_id}{colored_arrow}{colored_path}$ "
        command = input(prompt)
        if not execute_command(command):
            break

if __name__ == "__main__":
    main()

