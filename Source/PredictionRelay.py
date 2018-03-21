import requests
import urllib3
from lxml import html

"""
Communicates with predictors

"""


def cam_sol():
    # , 'uMaintainLogin': '1', 'rcID': ''
    login = {'uName': 'cgarelli@ithaca.edu', 'uPassword': 'tarquin'}
    # log = login.encode("utf-8")

    base_url = "http://www-mvsoftware.ch.cam.ac.uk"
    log_in_url = "/index.php/login/do_login/"
    s = requests.session()
    open_this = urllib3.encode_multipart_formdata(login)
    url = base_url + log_in_url

    # s.auth = login
    # s.headers.update({'x-test': 'true'})

    # sign_in = s.post(url, data=login)
    cam_sol = "/index.php/camsolintrinsic"
    # private_request = s.post(base_url+cam_sol)
    # login_url = s.post(url, login)
    # print(login_url.text)
    # request = requests.s().post()

