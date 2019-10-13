import os

import hvac

VAULT_ADDRESS = "https://vault.entrydsm.hs.kr"
SERVICE_NAME = os.environ.get("SERVICE_NAME")

VAULT_TOKEN = os.environ.get("VAULT_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

RUN_ENV = os.environ.get("RUN_ENV")

PICTURE_DIR = os.path.dirname(__file__).replace("/avengers", "") + '/pics'

SIGNUP_EMAIL_TEMPLATE_A = """
<head> <style type="text/css" title="x-apple-mail-formatting"></style> <meta name="viewport" content="width = 375, initial-scale = -1" /> <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> <meta charset="UTF-8" /> <title></title> <style> /* ------------------------------------- RESPONSIVENESS !importants in here are necessary :/ ------------------------------------- */ @media only screen and (max-device-width: 700px) { .table-wrapper { margin-top: 0px !important; border-radius: 0px !important; } .header { border-radius: 0px !important; } } </style></head><body style='-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;margin:0;padding:0;font-family:"Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;font-size:100%;line-height:1.6'> <table style="background: #F5F6F7;" width="100%" cellpadding="0" cellspacing="0" > <tbody> <tr> <td> <!-- body --> <table cellpadding="0" cellspacing="0" class="table-wrapper" style="margin:auto;margin-top:50px;border-radius:7px;-webkit-border-radius:7px;-moz-border-radius:7px;max-width:700px !important;box-shadow:0 8px 20px #e3e7ea !important;-webkit-box-shadow:0 8px 20px #e3e7ea !important;-moz-box-shadow:0 8px 20px #e3e7ea !important;box-shadow: 0 8px 20px #e3e7ea !important; -webkit-box-shadow: 0 8px 20px #e3e7ea !important; -moz-box-shadow: 0 8px 20px #e3e7ea !important;" > <tbody> <tr> <!-- Brand Header --> <td class="container" bgcolor="#FFFFFF" style="display:block !important;margin:0 auto !important;clear:both !important" > <img src="https://i.imgur.com/LQ5qSmC.png" style="max-width:100%" /> </td> </tr> <tr> <td class="container content" bgcolor="#FFFFFF" style="padding:35px 40px;border-bottom-left-radius:6px;border-bottom-right-radius:6px;display:block !important;margin:0 auto !important;clear:both !important" > <!-- content --> <div class="content-box" style="max-width:600px;margin:0 auto;display:block" > <!--Email template: myTeachable Confirmation Instructions (When No School is Set)Description: This email is sent when someone signs up or updates their email for a centralized Teachable Account.--> <!-- Content --> <h1 style='font-family:"Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;margin-bottom:15px;color:#47505E;margin:0px 0 10px;line-height:1.2;font-weight:200;font-size:28px;font-weight:bold;margin-bottom:30px' > 원서접수를 위해 이메일 주소를 인증해 주세요 </h1> <p style='font-weight:normal;padding:0;font-family:"Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;line-height:1.7;margin-bottom:1.3em;font-size:15px;color:#47505E' > 본 이메일에 적힌 코드는 3분간 유효합니다. 3분이 지났다면 다시 회원가입을 진행하셔야 합니다. </p> <center> <input class="confirmation-url btn-primary" style='color:#1EA69A;word-wrap:break-word;font-family:"Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;text-decoration:none;background-color:#ffffff;border:solid #65bbb7;line-height:2;max-width:100%;font-size:17px;padding:8px 40px 8px 40px;margin-top:30px;margin-bottom:30px;font-weight:bold;cursor:pointer;display:inline-block;border-radius:30px;margin-left:auto;margin-right:auto;text-align:center;color:#65bbb7 !important' value="
"""

SIGNUP_EMAIL_TEMPLATE_B = """
" readonly /> </center> <p style='font-weight:normal;padding:0;font-family:"Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;line-height:1.7;margin-bottom:1.3em;font-size:15px;color:#47505E' > 감사합니다,<br /> EntryDSM 팀 </p> </div> <!-- /content --> </td> <td></td> </tr> </tbody> </table> <!-- /body --> <div class="footer" style="padding-top:30px;padding-bottom:55px;width:100%;text-align:center;clear:both !important" > <p style='font-weight:normal;padding:0;font-family:"Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;line-height:1.7;margin-bottom:1.3em;font-size:15px;color:#47505E;font-size:12px;color:#666;margin-top:0px' > © 2019 EntryDSM™, <a href="x-apple-data-detectors://0" dir="ltr" x-apple-data-detectors="true" x-apple-data-detectors-type="address" x-apple-data-detectors-result="0" style="color: rgb(102, 102, 102); -webkit-text-decoration-color: rgba(102, 102, 102, 0.258824);" >(34111) 대전광역시 유성구 가정북로 76(장동 23-9)</a > </p> <p class="social-icons" style='font-weight:normal;padding:0;font-family:"Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;line-height:1.7;margin-bottom:1.3em;font-size:15px;color:#47505E;font-size:12px;color:#666;padding-top:5px' > <a href="https://www.facebook.com/entrydsm" style='color:#1EA69A;word-wrap:break-word;font-family:"Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;font-weight:800;color:#999;color:#049075 !important' ><img width="25" src="https://cdn2.hubspot.net/hubfs/677576/email-fb.png" style="max-width:100%" /></a> </p> </div> </td> </tr> </tbody> </table></body>
"""

RESET_PW_EMAIL_TEMPLATE_A = """
<head> <style type="text/css" title="x-apple-mail-formatting"></style> <meta name="viewport" content="width = 375, initial-scale = -1" /> <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> <meta charset="UTF-8" /> <title></title> <style> /* ------------------------------------- RESPONSIVENESS !importants in here are necessary :/ ------------------------------------- */ @media only screen and (max-device-width: 700px) { .table-wrapper { margin-top: 0px !important; border-radius: 0px !important; } .header { border-radius: 0px !important; } } </style></head><body style='-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;margin:0;padding:0;font-family:"Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;font-size:100%;line-height:1.6'> <table style="background: #F5F6F7;" width="100%" cellpadding="0" cellspacing="0" > <tbody> <tr> <td> <!-- body --> <table cellpadding="0" cellspacing="0" class="table-wrapper" style="margin:auto;margin-top:50px;border-radius:7px;-webkit-border-radius:7px;-moz-border-radius:7px;max-width:700px !important;box-shadow:0 8px 20px #e3e7ea !important;-webkit-box-shadow:0 8px 20px #e3e7ea !important;-moz-box-shadow:0 8px 20px #e3e7ea !important;box-shadow: 0 8px 20px #e3e7ea !important; -webkit-box-shadow: 0 8px 20px #e3e7ea !important; -moz-box-shadow: 0 8px 20px #e3e7ea !important;" > <tbody> <tr> <!-- Brand Header --> <td class="container" bgcolor="#FFFFFF" style="display:block !important;margin:0 auto !important;clear:both !important" > <img src="https://i.imgur.com/LQ5qSmC.png" style="max-width:100%" /> </td> </tr> <tr> <td class="container content" bgcolor="#FFFFFF" style="padding:35px 40px;border-bottom-left-radius:6px;border-bottom-right-radius:6px;display:block !important;margin:0 auto !important;clear:both !important" > <!-- content --> <div class="content-box" style="max-width:600px;margin:0 auto;display:block" > <!--Email template: myTeachable Confirmation Instructions (When No School is Set)Description: This email is sent when someone signs up or updates their email for a centralized Teachable Account.--> <!-- Content --> <h1 style='font-family:"Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;margin-bottom:15px;color:#47505E;margin:0px 0 10px;line-height:1.2;font-weight:200;font-size:28px;font-weight:bold;margin-bottom:30px' > 비밀번호를 변경하기 위해 이메일 주소를 인증해 주세요 </h1> <p style='font-weight:normal;padding:0;font-family:"Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;line-height:1.7;margin-bottom:1.3em;font-size:15px;color:#47505E' > 비밀번호를 변경하기 위해 아래 적힌 코드를 입력해 주세요. </p> <center> <input class="confirmation-url btn-primary" style='color:#1EA69A;word-wrap:break-word;font-family:"Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;text-decoration:none;background-color:#ffffff;border:solid #65bbb7;line-height:2;max-width:100%;font-size:17px;padding:8px 40px 8px 40px;margin-top:30px;margin-bottom:30px;font-weight:bold;cursor:pointer;display:inline-block;border-radius:30px;margin-left:auto;margin-right:auto;text-align:center;color:#65bbb7 !important' value="
"""

RESET_PW_EMAIL_TEMPLATE_B = """
" readonly /> </center> <p style='font-weight:normal;padding:0;font-family:"Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;line-height:1.7;margin-bottom:1.3em;font-size:15px;color:#47505E' > 감사합니다,<br /> EntryDSM 팀 </p> </div> <!-- /content --> </td> <td></td> </tr> </tbody> </table> <!-- /body --> <div class="footer" style="padding-top:30px;padding-bottom:55px;width:100%;text-align:center;clear:both !important" > <p style='font-weight:normal;padding:0;font-family:"Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;line-height:1.7;margin-bottom:1.3em;font-size:15px;color:#47505E;font-size:12px;color:#666;margin-top:0px' > © 2019 EntryDSM™, <a href="x-apple-data-detectors://0" dir="ltr" x-apple-data-detectors="true" x-apple-data-detectors-type="address" x-apple-data-detectors-result="0" style="color: rgb(102, 102, 102); -webkit-text-decoration-color: rgba(102, 102, 102, 0.258824);" >(34111) 대전광역시 유성구 가정북로 76(장동 23-9)</a > </p> <p class="social-icons" style='font-weight:normal;padding:0;font-family:"Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;line-height:1.7;margin-bottom:1.3em;font-size:15px;color:#47505E;font-size:12px;color:#666;padding-top:5px' > <a href="https://www.facebook.com/entrydsm" style='color:#1EA69A;word-wrap:break-word;font-family:"Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;font-weight:800;color:#999;color:#049075 !important' ><img width="25" src="https://cdn2.hubspot.net/hubfs/677576/email-fb.png" style="max-width:100%" /></a> </p> </div> </td> </tr> </tbody> </table></body>
"""

LOGO = """
──────────────▐█████───────
──────▄▄████████████▄──────
────▄██▀▀────▐███▐████▄────
──▄██▀───────███▌▐██─▀██▄──
─▐██────────▐███─▐██───██▌─
─██▌────────███▌─▐██───▐██─
▐██────────▐███──▐██────██▌
██▌────────███▌──▐██────▐██
██▌───────▐███───▐██────▐██
██▌───────███▌──▄─▀█────▐██
██▌──────▐████████▄─────▐██
██▌──────█████████▀─────▐██
▐██─────▐██▌────▀─▄█────██▌
─██▌────███─────▄███───▐██─
─▐██▄──▐██▌───────────▄██▌─
──▀███─███─────────▄▄███▀──
──────▐██▌─▀█████████▀▀────
──────███──────────────────                                                
"""


class VaultClient:
    _database_credential = None

    @classmethod
    def initialize(cls):
        cls.client = hvac.Client(url=VAULT_ADDRESS)

        if VAULT_TOKEN:
            cls.client.token = VAULT_TOKEN
        elif GITHUB_TOKEN:
            cls.client.auth.github.login(token=GITHUB_TOKEN)

    def __getattr__(self, item):
        try:
            data = self.client.read(
                f"service-secret/{RUN_ENV}/{SERVICE_NAME}"
            )["data"]
            return data[item]
        except (KeyError, TypeError):
            raise Exception(
                f"request on: service-secret/{RUN_ENV}/{SERVICE_NAME} \nrequested key {item} is can't be fetched"
            )
        except Exception as e:
            raise e


class Setting:
    def __init__(self, vault_client: VaultClient):
        self.vault_client = vault_client

    def __getattr__(self, item):
        return self.vault_client.__getattr__(item)

    @property
    def database_connection_info(self):
        return {
            "use_unicode": True,
            "charset": "utf8mb4",
            "user": self.vault_client.MYSQL_USERNAME,
            "password": self.vault_client.MYSQL_PASSWORD,
            "db": self.vault_client.MYSQL_DATABASE,
            "host": self.vault_client.MYSQL_HOST,
            "port": self.vault_client.MYSQL_PORT,
            "loop": None,
            "autocommit": True,
        }

    @property
    def cache_connection_info(self):
        return {
            "address": f"redis://:{self.vault_client.REDIS_PASSWORD}@{self.vault_client.REDIS_HOST}:{self.vault_client.REDIS_PORT}",
            # pylint: disable=line-too-long
            "minsize": 5,
            "maxsize": 10,
        }

    DEBUG = False if RUN_ENV == "prod" else True


settings = Setting(VaultClient())  # pylint: disable=invalid-name
