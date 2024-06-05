
import sys
import bs4
import aiohttp
import asyncio

async def gather_data(user,repo):
    async with aiohttp.ClientSession() as sess:
        async with sess.get("https://github.com/%s/%s"%(user,repo)) as rsp:
            body = await rsp.content.read()
    soup = bs4.BeautifulSoup(body, features = "html.parser")
    star_element = soup.find(attrs={"id":"repo-stars-counter-star"})
    return int(star_element.text) if star_element else 0

async def scrape(repos):
    return await asyncio.gather(*[gather_data(user,repo) for user,repo in repos])

if __name__ == "__main__":
    try:
        _,*repos = sys.argv
        repos = [(user,repo) for user,repo in [i.split("/") for i in repos]]
    except ValueError as ve:
        print("Usage: ghrank.py [REPOSITORIES]")
        sys.exit(1)

    stars = asyncio.run(scrape(repos))
    data = [(user,repo,starcount) for ((user,repo),starcount) in zip(repos,stars)]
    data.sort(key = lambda x: -x[2])
    for user,repo,starcount in data:
        print(f"{user}/{repo}:\t{starcount}⭐")
