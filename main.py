from os import popen
from marionette_driver.marionette import Marionette
from marionette_driver.wait import Wait as marionette_wait
from marionette_driver import By as marionette_by
from marionette_driver import expected

def get_marionette_port_from_user_config(tor_user_profile_directory:str) -> int:
    marionette_port = 2828  # Default port
    with open(tor_user_profile_directory+"user.js", 'r') as tor_user_config_file:
        for line in tor_user_config_file:
            if line.__contains__("\"marionette.port\","):
                marionette_port = int(line.split(' ')[-1].split(')')[0])
                break
    return marionette_port

def wait_for_page_url(client,url:str, timeout=30,):
    marionette_wait(client, timeout).until(lambda c: c.execute_script("return document.location.href") == url)

def twitter_auth(username:str,password:str):
    tor_browser_directory = "/home/deathonarrival/.local/opt/tor-browser/app/Browser/"
    tor_browser_executable_path = tor_browser_directory + "start-tor-browser"
    tor_user_profile_directory = tor_browser_directory + "TorBrowser/Data/Browser/profile.default/"

    tor_marionette_port = get_marionette_port_from_user_config(tor_user_profile_directory=tor_user_profile_directory)

    if Marionette.check_port_available(tor_marionette_port):
        print(f"Port {tor_marionette_port} is available! Setting is as Tor marionette port")
    else:
        print(f"Tor marionette port {tor_marionette_port} set in Tor config is unavailable. Provide custom port here as input, in args as <--marionette-port> or in Tor browser's about:config")
        print("Error occured, aborting")
        return

    popen(f"{tor_browser_executable_path} -marionette")

    client = Marionette(port=tor_marionette_port)
    client.start_session()
    client.maximize_window()
    wait_for_page_url(client=client,url="about:blank")

    client.navigate("https://twitter.com/login/")

    marionette_wait(client,30).until(expected.element_present(marionette_by.NAME,"text"))
    namefield = client.find_element(marionette_by.NAME,"text")
    marionette_wait(client,30).until(expected.element_displayed(namefield))
    namefield.clear()
    namefield.send_keys(username)

    weird_button_class_name = "css-18t94o4 css-1dbjc4n r-1m3jxhj r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu"
    button = client.find_element(marionette_by.CLASS_NAME,weird_button_class_name)
    print(button)
    button.click()

    marionette_wait(client,30).until(expected.element_present(marionette_by.NAME,"password"))
    passwordfield = client.find_element(marionette_by.NAME,"password")
    marionette_wait(client,30).until(expected.element_displayed(passwordfield))
    passwordfield.clear()
    passwordfield.send_keys(password)

    weird_button_class_name = "css-18t94o4 css-1dbjc4n r-1m3jxhj r-sdzlij r-1phboty r-rs99b7 r-19yznuf r-64el8z r-1ny4l3l r-1dye5f7 r-o7ynqc r-6416eg r-lrvibr"
    button = client.find_element(marionette_by.CLASS_NAME,weird_button_class_name)
    button.click()

    wait_for_page_url(client=client,url="https://twitter.com/home")

    weird_button_class_name = "css-18t94o4 css-1dbjc4n r-1sw30gj r-42olwf r-sdzlij r-1phboty r-rs99b7 r-18kxxzh r-1q142lx r-eu3ka r-5oul0u r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-lif3th"
    marionette_wait(client,30).until(expected.element_present(marionette_by.CLASS_NAME,weird_button_class_name))
    button = client.find_element(marionette_by.CLASS_NAME,weird_button_class_name)
    button.click()


if __name__ == '__main__':
    twitter_auth("""place auth data here!""")
else:
    print("damn, it fucked up!")