from mastodon import Mastodon
from os import path

"""
アプリケーションの登録とアカウントへの認証を行う
"""
PATH = path.dirname(path.abspath(__file__)) + "/"

def create_app(file_name, api_url):
    """
    アプリケーションを登録する
    """
    Mastodon.create_app(
        client_name = "mastodon-rendaino-tombstone",
        scopes = ["read", "write", "follow"],
        website = "https://github.com/kelvin27315/mastodon-rendaino-tombstone",
        to_file = PATH + file_name,
        api_base_url = api_url
    )

def log_in(client_file_neme, api_url, mail, password, user_file_name):
    """
    アカウントの認証を通す
    """
    mastodon = Mastodon(
        client_id = PATH + client_file_neme,
        api_base_url = api_url
    )
    mastodon.log_in(
        mail,
        password,
        scopes = ["read", "write", "follow"],
        to_file = PATH + user_file_name
    )

if __name__ == "__main__":
    #gensokyo.cloud
    create_app("clientcred_cloud.secret", "https://gensokyo.cloud")
    log_in(
        "clientcred_cloud.secret",
        "https://gensokyo.cloud",
        "*****@example.com",
        "*****",
        "usercred_cloud.secret"
    )
    #gensokyo.town
    create_app("clientcred.secret", "https://gensokyo.town")
    log_in(
        "clientcred.secret",
        "https://gensokyo.town",
        "*****@example.com",
        "*****",
        "usercred.secret"
    )
