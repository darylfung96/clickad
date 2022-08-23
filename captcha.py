from python3_anticaptcha import ImageToTextTask
import tempfile
import base64
import os


def solve_captcha(image_base64):
    """

    :param image_file:  base 64
    :return:
    """
    captcha_info = ImageToTextTask.ImageToTextTask(anticaptcha_key=os.environ['ANTICAPTCHA_KEY']).captcha_handler(captcha_base64=image_base64)
    # {'errorId': 10, 'errorCode': 'ERROR_ZERO_BALANCE', 'errorDescription': 'Account has zero or negative balance'}
    if captcha_info['errorId'] != 0:
        captcha_text = None
        print("Error: " + captcha_info['errorCode'])
    else:
        captcha_text = captcha_info['solution']['text']
        print("Captcha text: ", captcha_text)

    return captcha_text

# def solve_captcha(image_base64):
#     """
#
#     :param image_file:  base 64
#     :return:
#     """
#     # Specify softId to earn 10% commission with your app.
#     # Get your softId here: https://anti-captcha.com/clients/tools/devcenter
#     solver.set_soft_id(0)
#
#     tmp = tempfile.NamedTemporaryFile(delete=False)
#     try:
#         tmp.write(base64.decodebytes(bytes(image_base64, 'ascii')))
#         tmp.close()
#         captcha_text = solver.solve_and_return_solution(tmp.name)
#         if captcha_text != 0:
#             print("captcha text " + captcha_text)
#         else:
#             print("task finished with error " + solver.error_code)
#     finally:
#         os.remove(tmp.name)
#
#     return captcha_text