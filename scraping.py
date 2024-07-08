import requests
from random import randint
from threading import Thread, Lock


QUOTE = '\"'
top_prefix = "https://myanimelist.net/topanime.php?limit="
mal_prefix = "\"https://myanimelist.net/anime/"
# trailer_prefix: str = '\"https://www.youtube.com/embed'


def buildlps(pattern: str) :
    
    lps = [0]
    j = 0
    for i,char in enumerate(pattern) :
        if i == 0 : continue
        while pattern[j] != char and j > 0:
            j = lps[j - 1]
        if char == pattern[j] :
            j += 1
        lps.append(j)
        
    return lps

def kmp(pattern, text) :
    lps = buildlps(pattern)
    j = 0
    ans = []
    for i,char in enumerate(text) :
        
        while char != pattern[j] and j > 0:
            j = lps[j - 1]
        if char == pattern[j] :
            j += 1
            if j == len(pattern) :
                j = lps[j - 1]
                ans.append(i - len(pattern) + 1)
    
    return ans

def get_random_valid_anime_url() -> str :
    limit = randint(0, 5000)
    top_response = requests.get(top_prefix + str(limit))
    ind = kmp(mal_prefix, top_response.text)
    
    for idx in ind :
        if top_response.text[idx + len(mal_prefix)].isnumeric() :
            p = 1
            while(top_response.text[idx + p] != QUOTE) :
                p += 1
            return top_response.text[idx + 1 : idx + p]


def get_N_random_anime_urls(N: int) -> list[str] :
    
    assert N <= 10 # do not overdo threading
    
    lock = Lock()
    res = []
    def worker() :
        url = get_random_valid_anime_url()
        with lock :
            res.append(url)

    threads = []
    for i in range(N) :
        t = Thread(target=worker)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    return res

if __name__ == "__main__" :
    n = int(input("How many urls do you want (n <= 10): "))
    for url in get_N_random_anime_urls(n) :
        print(url)