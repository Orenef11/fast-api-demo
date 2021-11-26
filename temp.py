# import requests
#
# from app.consts import HEADERS
#
# # import requests
# #
# # headers = {
# #     'Accept': 'application/json',
# #     'Content-Type': 'application/json',
# #     'Authorization': 'Bearer ACCESS-TOKEN',
# # }
# #
# #
# # response = requests.post('https://gorest.co.in/public/v1/users', headers=headers, data=data)
#
# # response = requests.post('https://gorest.co.in/public/v1/users', headers=headers, data=data)
# # response = requests.patch('https://gorest.co.in/public/v1/users/123', headers=HEADERS, data=data)
# from app.tools.models import User
#
# 3166
# 3195
# User
# from pydantic import BaseModel
#
#
# class User(BaseModel):
#     name: str
#     email: str
#     gender: str
#     status: str
#
# response = requests.delete('http://127.0.0.1:8000/public/v1/users/3354', headers=HEADERS)
# aa = User(name="test test1",
#           email="111111test.aaa11@15ce1.com",
#           gender="male",
#           status="active")
# response = requests.post('http://127.0.0.1:8000/users', headers=HEADERS, data=aa.json())
# aa = User(name="Tenali Ramafsdf1",
#           email="s2342342tenali.rkrisasd1@15ce.com",
#           gender="male",
#           status="active")
# response = requests.put('http://127.0.0.1:8000/users/3354', headers=HEADERS, data=aa)
# response = requests.delete('http://127.0.0.1:8000/users/3354', headers=HEADERS)
# print(response.json())
