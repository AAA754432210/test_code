from .base_page import BasePage


class LoginHomePage(BasePage):
    """
    登录设备管理系统
    """
    # config = configparser.ConfigParser()
    # file_path = os.path.dirname(os.path.abspath('.')) + '/config/password.ini'
    # config.read(file_path)
    # username = config.get("userName", "username")
    # password = config.get("passWord", "password")
    user_link = "xpath=>/html/body/div[3]/div/ul/li[1]/input"
    pass_link = "xpath=>/html/body/div[3]/div/ul/li[2]/input"
    login_link = 'xpath=>//*[@id="loginId"]'

    # user_link = "c => loginuser"
    # pass_link = "c => loginpwd"

    def set_username(self, username):
        admin_user = self.find_element(self.user_link)
        admin_user.send_keys(username)
        # self.wait(1)

    def set_password(self, password):
        admin_pass = self.find_element(self.pass_link)
        admin_pass.send_keys(password)
        # self.wait(1)

    def click_login(self):
        self.click(self.login_link)
        self.sleep(3)

    def is_login_sucess(self):
        return self.is_visible('//*[@id="msg"]')
    # //*[@id="msg"]