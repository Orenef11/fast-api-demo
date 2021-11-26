# import asyncio
# from typing import Dict, Any, List
#
# import aiohttp
#
# from app.consts import GO_REST_BASIC_URL
# from app.tools.parallelism import BaseMultipleRequests
#
#
# class UsersGenerator(BaseMultipleRequests):
#     url: str = f"{GO_REST_BASIC_URL}/users"
#     pagination_url: str = url.format("?page={}")
#
#     def get_all_users(self) -> List[Dict[str, Any]]:
#         """
#         Extract all users details from all available pages
#         """
#         urls = [
#             self.pagination_url.format(page_idx)
#             for page_idx in range(1, self.pagination_details()["pagination"]["pages"] + 1)
#         ]
#         return self.run_multiple_urls(urls=urls)
#
#     async def get_user(self, user_id: int) -> Dict[str, Any]:
#         """
#         Extract user details by user-id
#         """
#         async with aiohttp.ClientSession() as session:
#             return await self.fetch(session, self.url.format(user_id + f"?"))
