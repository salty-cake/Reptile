#同步操作:拿到所有章节的herf和标题
#异步操作:访问章节url下载文章内容
import requests
from lxml import etree 
import aiohttp
import aiofiles
import asyncio
'''为了防止async报错'''
import nest_asyncio
nest_asyncio.apply()

async def aiodownload(name,href):
    child_url=novel_url+href
    headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71",
              "referer": "https://www.23qb.com/book/22433/"
              }
    async with aiohttp.ClientSession() as session:
        async with session.get(child_url,headers=headers) as resp:
            text=await resp.text()
            child_tree=etree.HTML(text)
            sentences=child_tree.xpath('//*[@id="TextContent"]/p/text()')
            #文件路径自己设置，每章节保存一个文件
            async with aiofiles.open('D:/projects/爬虫/铅笔小说/qb_novel/'+name,mode='w',encoding='gbk') as f:
                for sentence in sentences:
                    await f.write(sentence+'\n')
                print(name,'完成')
    
    
async def get_chapter_herf(url): #给一部小说的主网址
    resp=requests.get(url)
    tree=etree.HTML(resp.text)
    details=tree.xpath('/html/body/div[3]/div[3]/ul[2]/li')
    tasks=[]
    for detail in details:
        name=detail.xpath('./a/text()')[0]
        herf=detail.xpath('./a/@href')[0].split('/')[-1]
        #准备异步任务
        tasks.append(asyncio.create_task(aiodownload(name,herf)))
        
    await asyncio.wait(tasks)
    resp.close()



if __name__=='__main__':
    novel_url="https://www.23qb.com/book/22433/" #小说的主页面
    asyncio.run(get_chapter_herf(novel_url))
    print('all over!')