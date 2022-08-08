from anticaptchaofficial.imagecaptcha import *
import tempfile
import base64

solver = imagecaptcha()
solver.set_verbose(1)
solver.set_key("ac51a145f8d0aff8399be9b45fbbdaa1")


def solve_captcha(image_base64):
    """

    :param image_file:  base 64
    :return:
    """
    # Specify softId to earn 10% commission with your app.
    # Get your softId here: https://anti-captcha.com/clients/tools/devcenter
    solver.set_soft_id(0)

    tmp = tempfile.NamedTemporaryFile(mode='w')

    with open(tmp.name, 'wb') as f:
        f.write(base64.decodebytes(bytes(image_base64, 'ascii')))

    captcha_text = solver.solve_and_return_solution(tmp.name)
    if captcha_text != 0:
        print("captcha text " + captcha_text)
    else:
        print("task finished with error " + solver.error_code)
    return captcha_text