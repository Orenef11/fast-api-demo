# import asyncio
# import datetime
# from typing import Dict, Any, List
#
# import aiohttp
# import requests
# from aiohttp import ClientSession, ClientResponseError
# from requests import RequestException
# from tenacity import retry, stop_after_attempt, wait_fixed, wait_random_exponential, retry_if_exception_type
#
#
# class BaseMultipleRequests:
#     url: str
#     pagination_url: str
#     headers: Dict[str, str] = {
#         'Accept': 'application/json',
#         'Content-Type': 'application/json',
#     }
#
#     def __init__(self):
#         self.loop = asyncio.get_event_loop()
#
#     def pagination_details(self) -> Dict[str, Any]:
#         res = requests.get(url=self.pagination_url.format(1), headers=self.headers)
#         res.raise_for_status()
#         return res.json()["meta"]
#
#     @retry(reraise=True, retry=retry_if_exception_type(ClientResponseError),
#            wait=wait_random_exponential(multiplier=1, max=60))
#     async def fetch(self, session: ClientSession, url: str, raise_for_status: bool = True) -> Dict[str, Any]:
#         start_time = datetime.datetime.now()
#         print(f"%s, %s" % (start_time, url))
#         async with session.get(url, raise_for_status=raise_for_status, headers=self.headers) as response:
#             try:
#                 await response.json()
#             except RequestException:
#                 return {"status_code": response.status_code, "error_msg": response.reason}
#
#     async def _run_multiple_urls(self, urls: List[str]):
#         async with aiohttp.ClientSession() as session:
#             return await asyncio.gather(*[self.fetch(session, url) for url in urls])
#
#     def run_multiple_urls(self, urls) -> List[Dict[str, Any]]:
#         return self.loop.run_until_complete(self._run_multiple_urls(urls))
#
#     def __delete__(self, instance):
#         print("clear")
#         instance.loop.close()
#
#
# if __name__ == '__main__':
#     urls = [f"https://gorest.co.in/public/v1/users?page={page_idx}" for page_idx in range(1, 20)]
#     BaseMultipleRequests().run_multiple_urls(urls)
