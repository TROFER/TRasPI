import json
import urllib.request

import core

from app import App


class Ticker:

    URL = "https://api.cryptonator.com/api/ticker/"

    def request(self, code):
        try:
            request = urllib.request.Request(f"{self.URL}{code}", headers={
                                             'User-Agent': 'Mozilla/5.0'})
            return json.load(urllib.request.urlopen(request))
        except:
            return None


class Pool:

    URL = "https://api.nanopool.org/v1/xmr/"

    def __init__(self):
        with open(f"{core.sys.const.path}user/wallet_address.txt") as file:
            self.wallet_address = file.read().replace("\n", "")

    def request(self, function, hours=None):
        try:
            if hours is None:
                request = urllib.request.Request(
                    f'{self.URL}{function}/{self.wallet_address}', headers={'User-Agent': 'Mozilla/5.0'})
            else:
                request = urllib.request.Request(
                    f'{self.URL}avghashratelimited/{self.wallet_address}/{hours}', headers={'User-Agent': 'Mozilla/5.0'})
            return json.load(urllib.request.urlopen(request))
        except BaseException as e:
            print(e)
            return None

    def balance(self):
        return "{:.8f}".format(float(self.request("balance")["data"]))

    def current_hashrate(self):
        return self.request("hashrate")["data"]

    def worker_count(self):
        count = 0
        for worker in self.request("workers")["data"]:
            if worker["hashrate"] > 0:
                count += 1
        return count

    def average_hashrate(self):
        return self.request("avghashrateworkers", hours=1)["data"]


ticker = Ticker()
pool = Pool()
