""" python http-client.py sync/async 3 https://requestb.in/1ljrfgy1 """

import requests
import time
import asyncio
import sys


async def async_call(loop, request_no, url):
    print("request{0} sent".format(request_no))
    future = loop.run_in_executor(None, requests.post, url)
    response = await future
    print("request{0} - {1} : {2}".format(request_no,
                                          response.status_code, response.content))


def sync_call(request_no, url):
    print("request{0} sent".format(request_no))
    r = requests.post(url, data={"ts": time.time()})
    print("request{0} - {1} : {2}".format(request_no,
                                          r.status_code, r.content))


if __name__ == "__main__":
    type_of_request = sys.argv[1]
    no_of_requests = sys.argv[2]
    url = sys.argv[3]
    if type_of_request == 'sync':
        for i in range(1, int(no_of_requests) + 1):
            sync_call(i, url)
    else:
        loop = asyncio.get_event_loop()
        task_list = []
        for i in range(1, int(no_of_requests) + 1):
            task_list.append(asyncio.ensure_future(async_call(loop, i, url)))
        loop.run_until_complete(asyncio.gather(*task_list))
        loop.close()
