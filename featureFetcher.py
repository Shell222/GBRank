# -*- coding:utf-8 -*-
import requests
import os,time
from multiprocessing import Process

PATH = '../data' 
DATA_SET = 'C:/Users/t-qixu/Desktop/disSource.csv'


class MyProcess(Process):
    def __init__(self, index, total, token):
        self.index = index
        self.total = total
        self.token = token
        Process.__init__(self)
 
    def run(self):
        print("P start >>> pid={0},ppid={1}".format(os.getpid(),os.getppid()))
        print("info index = {0}".format(self.index))
        with open(PATH + f'data{self.index}.txt', 'a') as output:
            with open(DATA_SET) as input:
                c = 0
                for line in input:
                    if c == self.index:
                        line = line.replace('\n', '')
                        data = call(line, self.token)
                        output.write(line + ',' + data + '\n')
                    c += 1
                    c %= self.total

        print("P end >>> pid={}".format(os.getpid()))
 
# def main():
#     print("主进程开始>>> pid={}".format(os.getpid()))
#     myp=MyProcess()
#     myp.start()
#     # myp.join()


def call(source, token):
    url = f'https://graph.microsoft.com/v1.0/users/{source}/manager'
    
    headers = {'Authorization': f"bearer {token}"}

    response = requests.get(url, headers = headers)

    if response.status_code != 200:
        print(source, response.json())
        return ""
    return response.json()['id']

def fetch_feature(index, token):
    pass


if __name__ == '__main__':
    start = 0
    my_token = "eyJ0eXAiOiJKV1QiLCJub25jZSI6IkFRQUJBQUFBQUFEWHpaM2lmci1HUmJEVDQ1ek5TRUZFVnpsempyWlBGNURUcGtUR3A4aWxjWXZEV051M0JWU0QtV2lZSzN6dXFKRXBPbzAzZ1V6TWVBeTAwOXNsT2ZySnprUjR1VmlPZnNyNi1HNjNTS1gxWkNBQSIsImFsZyI6IlJTMjU2IiwieDV0IjoiN19adWYxdHZrd0x4WWFIUzNxNmxValVZSUd3Iiwia2lkIjoiN19adWYxdHZrd0x4WWFIUzNxNmxValVZSUd3In0.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20vIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvNzJmOTg4YmYtODZmMS00MWFmLTkxYWItMmQ3Y2QwMTFkYjQ3LyIsImlhdCI6MTUzNDIyMzg3NCwibmJmIjoxNTM0MjIzODc0LCJleHAiOjE1MzQyMjc3NzQsImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBVVFBdS84SUFBQUFpZllnTjJsWER5RXpBcUYzOTlQQ1JSSjJkb3dqa29CSEpHQkpsSUF0WmZRZDNOVU9qTHVUeFB2Z2lsOFZwaUdIZERYbVpEV0s1WDZnVUlkSmFYSkxZQT09IiwiYW1yIjpbInJzYSIsIm1mYSJdLCJhcHBfZGlzcGxheW5hbWUiOiJ0bWdtIiwiYXBwaWQiOiJjNmFlNzY5MC0yNTU5LTRjMmUtOWVmYS04NTg3ZWJkZWYwMWMiLCJhcHBpZGFjciI6IjEiLCJkZXZpY2VpZCI6ImYyMjVjZmFhLTA5ZGEtNGQzMS1iNDQ5LTUzMzg4M2M2M2U2NCIsImVfZXhwIjoyNjI4MDAsImZhbWlseV9uYW1lIjoiWHUiLCJnaXZlbl9uYW1lIjoiUWl5dWFuIiwiaXBhZGRyIjoiMTY3LjIyMC4yMzIuODYiLCJuYW1lIjoiUWl5dWFuIFh1Iiwib2lkIjoiNWY4ZmQ1N2QtOWNhMS00Mzc4LTgwOWYtNjQzNzk1NDk0MzllIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTIxNDY3NzMwODUtOTAzMzYzMjg1LTcxOTM0NDcwNy0yMzY1Mzc0IiwicGxhdGYiOiIzIiwicHVpZCI6IjEwMDM3RkZFQUIwNTBEM0MiLCJzY3AiOiJCb29raW5ncy5NYW5hZ2UuQWxsIEJvb2tpbmdzLlJlYWQuQWxsIEJvb2tpbmdzLlJlYWRXcml0ZS5BbGwgQm9va2luZ3NBcHBvaW50bWVudC5SZWFkV3JpdGUuQWxsIENhbGVuZGFycy5SZWFkIENhbGVuZGFycy5SZWFkLlNoYXJlZCBDYWxlbmRhcnMuUmVhZFdyaXRlIENhbGVuZGFycy5SZWFkV3JpdGUuU2hhcmVkIENvbnRhY3RzLlJlYWQgQ29udGFjdHMuUmVhZC5TaGFyZWQgQ29udGFjdHMuUmVhZFdyaXRlIENvbnRhY3RzLlJlYWRXcml0ZS5BbGwgQ29udGFjdHMuUmVhZFdyaXRlLlNoYXJlZCBEZXZpY2UuQ29tbWFuZCBEZXZpY2UuUmVhZCBFQVMuQWNjZXNzQXNVc2VyLkFsbCBlbWFpbCBGaWxlcy5SZWFkIEZpbGVzLlJlYWQuQWxsIEZpbGVzLlJlYWQuU2VsZWN0ZWQgRmlsZXMuUmVhZFdyaXRlIEZpbGVzLlJlYWRXcml0ZS5BbGwgRmlsZXMuUmVhZFdyaXRlLkFwcEZvbGRlciBGaWxlcy5SZWFkV3JpdGUuU2VsZWN0ZWQgTWFpbC5SZWFkIE1haWwuUmVhZC5TaGFyZWQgTWFpbC5SZWFkV3JpdGUgTWFpbC5SZWFkV3JpdGUuU2hhcmVkIE1haWwuU2VuZCBNYWlsLlNlbmQuU2hhcmVkIE1haWxib3hTZXR0aW5ncy5SZWFkIE1haWxib3hTZXR0aW5ncy5SZWFkV3JpdGUgTm90ZXMuQ3JlYXRlIE5vdGVzLlJlYWRXcml0ZS5DcmVhdGVkQnlBcHAgb2ZmbGluZV9hY2Nlc3Mgb3BlbmlkIFBlb3BsZS5SZWFkIHByb2ZpbGUgU2l0ZXMuTWFuYWdlLkFsbCBTaXRlcy5SZWFkLkFsbCBTaXRlcy5SZWFkV3JpdGUuQWxsIFRhc2tzLlJlYWRXcml0ZSBVc2VyLlJlYWQgVXNlci5SZWFkQmFzaWMuQWxsIFVzZXIuUmVhZFdyaXRlIFVzZXJBY3Rpdml0eS5SZWFkV3JpdGUuQ3JlYXRlZEJ5QXBwIFVzZXJUaW1lbGluZUFjdGl2aXR5LldyaXRlLkNyZWF0ZWRCeUFwcCIsInNpZ25pbl9zdGF0ZSI6WyJkdmNfbW5nZCIsImR2Y19jbXAiLCJkdmNfZG1qZCIsImttc2kiXSwic3ViIjoiY0NBWHNlVXpzQXZ1VnQ5RUU1eHYxamFIMkxIRnM3RHRabld1cS1wVi1xVSIsInRpZCI6IjcyZjk4OGJmLTg2ZjEtNDFhZi05MWFiLTJkN2NkMDExZGI0NyIsInVuaXF1ZV9uYW1lIjoidC1xaXh1QG1pY3Jvc29mdC5jb20iLCJ1cG4iOiJ0LXFpeHVAbWljcm9zb2Z0LmNvbSIsInV0aSI6ImJsUFNSRUJuYzBteFpuTWRBdm9RQUEiLCJ2ZXIiOiIxLjAifQ.G6D_He5xWFxtbi98v1pEN0zmgP3exRekcRTZF5dP64oGwMGMbTmUaXUTlzDNPtK7_u6gWXWcNSgWMiyMZQIbemTyGFuqjpdmHFT_6ywNr8eYitmhu7m0Q6w4oUcVr7HziHAlpOkHyGfkTWv3qrhqHtyAVcjv-78W1CtQJLZWFqljYPVolo-4Lr1kJID9JI2BqKasFXvZE0asyLczc6P9ui0Um-ab4Kw2qzRV4eF5wyFZcA5bS2Iow2P2WyUja4HhResH0yIC0K7apljJRLy7QSS3Dx43jNu49mSPlyY3oifrOikVBLrjvZ6o5TCeGUG9N65lGeROGiY8keEZ3kaXaw"
    print(call(source = '0001a966-383d-4c8c-a0e9-c0c35ab5b3aa', token = my_token))
    # token = "eyJ0eXAiOiJKV1QiLCJub25jZSI6IkFRQUJBQUFBQUFEWHpaM2lmci1HUmJEVDQ1ek5TRUZFUzJkSVhCZ3JxTlhzZTJ6ODJqQ201N25ocG5nLXpyRnJ4Ymp5WThYOEw4UXloZVIxZXU4WVdzTUFDeEUzQ0llei03SDE3R1NBNTFFMWlmb1Zvek1WaFNBQSIsImFsZyI6IlJTMjU2IiwieDV0IjoiN19adWYxdHZrd0x4WWFIUzNxNmxValVZSUd3Iiwia2lkIjoiN19adWYxdHZrd0x4WWFIUzNxNmxValVZSUd3In0.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20vIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvNzJmOTg4YmYtODZmMS00MWFmLTkxYWItMmQ3Y2QwMTFkYjQ3LyIsImlhdCI6MTUzMzg4MzQ0OCwibmJmIjoxNTMzODgzNDQ4LCJleHAiOjE1MzM4ODczNDgsImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBVVFBdS84SUFBQUFCZE1OdCtZK1VjM08wRHdxSmg1Z2thSE9yMjIyS3dwa0dadUtLL1hQK2ZoNzUzb25UY1NVM0FYcFdKN0wwdjFndXEweTg2VHZ5QmEzak5TZkoyc01IZz09IiwiYW1yIjpbIndpYSIsIm1mYSJdLCJhcHBfZGlzcGxheW5hbWUiOiJ0bWdtIiwiYXBwaWQiOiJjNmFlNzY5MC0yNTU5LTRjMmUtOWVmYS04NTg3ZWJkZWYwMWMiLCJhcHBpZGFjciI6IjEiLCJkZXZpY2VpZCI6ImYyMjVjZmFhLTA5ZGEtNGQzMS1iNDQ5LTUzMzg4M2M2M2U2NCIsImVfZXhwIjoyNjI4MDAsImZhbWlseV9uYW1lIjoiWHUiLCJnaXZlbl9uYW1lIjoiUWl5dWFuIiwiaW5fY29ycCI6InRydWUiLCJpcGFkZHIiOiIxNjcuMjIwLjIzMi44NiIsIm5hbWUiOiJRaXl1YW4gWHUiLCJvaWQiOiI1ZjhmZDU3ZC05Y2ExLTQzNzgtODA5Zi02NDM3OTU0OTQzOWUiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtMjE0Njc3MzA4NS05MDMzNjMyODUtNzE5MzQ0NzA3LTIzNjUzNzQiLCJwbGF0ZiI6IjMiLCJwdWlkIjoiMTAwMzdGRkVBQjA1MEQzQyIsInNjcCI6IkJvb2tpbmdzLk1hbmFnZS5BbGwgQm9va2luZ3MuUmVhZC5BbGwgQm9va2luZ3MuUmVhZFdyaXRlLkFsbCBCb29raW5nc0FwcG9pbnRtZW50LlJlYWRXcml0ZS5BbGwgQ2FsZW5kYXJzLlJlYWQgQ2FsZW5kYXJzLlJlYWQuU2hhcmVkIENhbGVuZGFycy5SZWFkV3JpdGUgQ2FsZW5kYXJzLlJlYWRXcml0ZS5TaGFyZWQgQ29udGFjdHMuUmVhZCBDb250YWN0cy5SZWFkLlNoYXJlZCBDb250YWN0cy5SZWFkV3JpdGUgQ29udGFjdHMuUmVhZFdyaXRlLkFsbCBDb250YWN0cy5SZWFkV3JpdGUuU2hhcmVkIERldmljZS5Db21tYW5kIERldmljZS5SZWFkIEVBUy5BY2Nlc3NBc1VzZXIuQWxsIGVtYWlsIEZpbGVzLlJlYWQgRmlsZXMuUmVhZC5BbGwgRmlsZXMuUmVhZC5TZWxlY3RlZCBGaWxlcy5SZWFkV3JpdGUgRmlsZXMuUmVhZFdyaXRlLkFsbCBGaWxlcy5SZWFkV3JpdGUuQXBwRm9sZGVyIEZpbGVzLlJlYWRXcml0ZS5TZWxlY3RlZCBNYWlsLlJlYWQgTWFpbC5SZWFkLlNoYXJlZCBNYWlsLlJlYWRXcml0ZSBNYWlsLlJlYWRXcml0ZS5TaGFyZWQgTWFpbC5TZW5kIE1haWwuU2VuZC5TaGFyZWQgTWFpbGJveFNldHRpbmdzLlJlYWQgTWFpbGJveFNldHRpbmdzLlJlYWRXcml0ZSBOb3Rlcy5DcmVhdGUgTm90ZXMuUmVhZFdyaXRlLkNyZWF0ZWRCeUFwcCBvZmZsaW5lX2FjY2VzcyBvcGVuaWQgUGVvcGxlLlJlYWQgcHJvZmlsZSBTaXRlcy5NYW5hZ2UuQWxsIFNpdGVzLlJlYWQuQWxsIFNpdGVzLlJlYWRXcml0ZS5BbGwgVGFza3MuUmVhZFdyaXRlIFVzZXIuUmVhZCBVc2VyLlJlYWRCYXNpYy5BbGwgVXNlci5SZWFkV3JpdGUgVXNlckFjdGl2aXR5LlJlYWRXcml0ZS5DcmVhdGVkQnlBcHAgVXNlclRpbWVsaW5lQWN0aXZpdHkuV3JpdGUuQ3JlYXRlZEJ5QXBwIiwic2lnbmluX3N0YXRlIjpbImR2Y19tbmdkIiwiZHZjX2NtcCIsImR2Y19kbWpkIiwia21zaSJdLCJzdWIiOiJjQ0FYc2VVenNBdnVWdDlFRTV4djFqYUgyTEhGczdEdFpuV3VxLXBWLXFVIiwidGlkIjoiNzJmOTg4YmYtODZmMS00MWFmLTkxYWItMmQ3Y2QwMTFkYjQ3IiwidW5pcXVlX25hbWUiOiJ0LXFpeHVAbWljcm9zb2Z0LmNvbSIsInVwbiI6InQtcWl4dUBtaWNyb3NvZnQuY29tIiwidXRpIjoicXgyLVc4N3YtRVdQVnRNckh4a0NBQSIsInZlciI6IjEuMCJ9.HJs213AIwygz4Ikf2rYp1dtwJTW2PJbfSBfZXzh_KopiGwpaNwFdanqtw03yDWjNSQ4QsQpIHkrkfvBU81f5q01yk482mtnmXmLVYtSxA-ENv6r9_opgGi4kMYQ1fFLL4f6fkfGx4WCTXQbKCs17h6cYtAd6hg8x_LDhPHvK8AgfzmhBsGmIEuNkMcO12EP4xEoBv7EnYotO3ZB6BwlbRvZ4V37aPUwyHI4wfVkXpPYH_xa2inI7DKFEeT790rRf-rNZaXFmatw8RjGKJQ3pIB4AJtpUlnFMOzAZPM6rLMD0CXzPSMaDbmVAiaIcWEdCegKFKj6TBi_3sjIb9RnITA"
    # pl = [MyProcess(i, 6, token) for i in range(6)]
    # for i in pl:
    #     i.start()
    # for i in pl:
    #     i.join()

    