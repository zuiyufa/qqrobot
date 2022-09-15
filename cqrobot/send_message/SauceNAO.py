print("0")
import sys
print("1")
import requests
print("2")
import json
print("3")
import codecs
print("4")
import re
print("5")
import time
print("6")
from collections import OrderedDict
print("7")
# sys.stdout = codecs.getwriter('utf8')(sys.stdout.detach())
print("8")
# sys.stderr = codecs.getwriter('utf8')(sys.stderr.detach())
print("9")
index_hmags='0'
index_reserved='0'
index_hcg='0'
index_ddbobjects='0'
index_ddbsamples='0'
index_pixiv='1'
index_pixivhistorical='1'
index_reserved='0'
index_seigaillust='1'
index_danbooru='1'
index_drawr='1'
index_nijie='1'
index_yandere='0'
index_animeop='0'
index_reserved='0'
index_shutterstock='0'
index_fakku='0'
index_hmisc='0'
index_2dmarket='0'
index_medibang='0'
index_anime='0'
index_hanime='0'
index_movies='0'
index_shows='0'
index_gelbooru='0'
index_konachan='0'
index_sankaku='0'
index_animepictures='0'
index_e621='0'
index_idolcomplex='0'
index_bcyillust='0'
index_bcycosplay='0'
index_portalgraphics='0'
index_da='1'
index_pawoo='0'
index_madokami='0'
index_mangadex='0'
db_bitmask = int(index_mangadex+index_madokami+index_pawoo+index_da+index_portalgraphics+index_bcycosplay+index_bcyillust+index_idolcomplex+index_e621+index_animepictures+index_sankaku+index_konachan+index_gelbooru+index_shows+index_movies+index_hanime+index_anime+index_medibang+index_2dmarket+index_hmisc+index_fakku+index_shutterstock+index_reserved+index_animeop+index_yandere+index_nijie+index_drawr+index_danbooru+index_seigaillust+index_anime+index_pixivhistorical+index_pixiv+index_ddbsamples+index_ddbobjects+index_hcg+index_hanime+index_hmags,2)
minsim='80!'
shortremain = ""
longremain = ""
similarity = ""
print("1")
def SauceNao(msg):
    # print(msg)#-----------------------------------------------------------------------------------------------
    image_url=msg.split("=",3)[-1].split("]")[0]
    # print(image_url)#-------------------------------------------------------------------------------------------------------
    params = {"url": image_url,
              "dbmask":db_bitmask,
              "api_key": "ac68e3019aa148579c40bafee9975e82f1f87ec0",
              "output_type": 2,
              "numres": 1,
              "minsim":minsim
              }
    url='http://saucenao.com/search.php'
    processResults = True
    while True:
        r=requests.post(url,params=params)
        if r.status_code != 200:
            if r.status_code == 403:
                print('Incorrect or Invalid API Key! Please Edit Script to Configure...')
                sys.exit(1)
            else:
                # generally non 200 statuses are due to either overloaded servers or the user is out of searches
                print("status code: " + str(r.status_code))
                time.sleep(10)
        else:
            results = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(r.text)
            if int(results['header']['user_id']) > 0:
                # api responded
                print('Remaining Searches 30s|24h: ' + str(results['header']['short_remaining']) + '|' + str(
                    results['header']['long_remaining']))
                shortremain = str(results['header']['short_remaining'])
                longremain = str(results['header']['long_remaining'])
                if int(results['header']['status']) == 0:
                    # search succeeded for all indexes, results usable
                    break
                else:
                    if int(results['header']['status']) > 0:
                        # One or more indexes are having an issue.
                        # This search is considered partially successful, even if all indexes failed, so is still counted against your limit.
                        # The error may be transient, but because we don't want to waste searches, allow time for recovery.
                        print('API Error. Retrying in 30 seconds...')
                        time.sleep(30)
                    else:
                        # Problem with search as submitted, bad image, or impossible request.
                        # Issue is unclear, so don't flood requests.
                        print('Bad image or other request error. Skipping in 10 seconds...')
                        processResults = False
                        time.sleep(10)
                        break
            else:
                # General issue, api did not respond. Normal site took over for this error state.
                # Issue is unclear, so don't flood requests.
                print('Bad image, or API failure. Skipping in 10 seconds...')
                processResults = False
                time.sleep(10)
                break
    if processResults:
        print(results)
        if int(results['header']['results_returned']) > 0:
            # one or more results were returned
            if float(results['results'][0]['header']['similarity']) > float(results['header']['minimum_similarity']):
                print('hit! ' + str(results['results'][0]['header']['similarity']))
                similarity=str(results['results'][0]['header']['similarity'])
                # get vars to use
                service_name = ''
                illust_id = 0
                member_id = -1
                index_id = results['results'][0]['header']['index_id']
                page_string = ''
                page_match = re.search('(_p[\d]+)\.', results['results'][0]['header']['thumbnail'])
                min_img_url=results['results'][0]['header']['thumbnail']
                if page_match:
                    page_string = page_match.group(1)

                if index_id == 5 or index_id == 6:
                    # 5->pixiv 6->pixiv historical
                    service_name = 'pixiv'
                    member_id = results['results'][0]['data']['member_id']
                    illust_id = results['results'][0]['data']['pixiv_id']
                    img_url = results['results'][0]['data']['ext_urls']
                    img_title = results['results'][0]['data']['title']
                elif index_id == 8:
                    # 8->nico nico seiga
                    service_name = 'Nico Nico seiga'
                    member_id = results['results'][0]['data']['member_id']
                    illust_id = results['results'][0]['data']['seiga_id']
                    img_url=results['results'][0]['data']['ext_urls']
                    img_title=results['results'][0]['data']['title']
                elif index_id == 10:
                    # 10->drawr
                    service_name = 'drawr Images'
                    member_id = results['results'][0]['data']['member_id']
                    illust_id = results['results'][0]['data']['drawr_id']
                elif index_id == 11:
                    # 11->nijie
                    service_name = 'nijie Images'
                    member_id = results['results'][0]['data']['member_id']
                    illust_id = results['results'][0]['data']['nijie_id']
                    img_url=results['results'][0]['data']['ext_urls']
                    img_title=results['results'][0]['data']['title']
                elif index_id == 34:
                    # 34->da
                    service_name = 'deviantArt'
                    member_id=results['results'][0]['data']['author_name']
                    illust_id=results['results'][0]['data']['da_id']
                    img_url=results['results'][0]['data']['ext_urls']
                    img_title=results['results'][0]['data']['title']

                elif index_id == 9:
                    # 9->da
                    service_name = 'danbooru'
                    member_id=results['results'][0]['data']['danbooru_id']
                    illust_id=results['results'][0]['data']['gelbooru_id']
                    img_url=results['results'][0]['data']['source']
                    img_title=results['results'][0]['data']['characters']
                    # illust_id = results['results'][0]['data']['da_id']
                    # print("search ion danbooru")
    
                else:
                    # unknown
                    print('Unhandled Index! Exiting...')
                    return[True,"未能处理的搜索结果"]
                try:
                    if member_id >= 0:
                        if index_id == 5 or index_id == 6 or index_id==9 or index_id==34 or index_id==8 or index_id==11:
                            img_msg ="搜索平台："+service_name+"  相似度为"+str(similarity)+"\n"+"标题："+img_title+"[CQ:image,file="+str(min_img_url)+"]"+"PID："+str(illust_id)+"\n"+"UID："+str(member_id)+"\n"+"地址:\n\n"+str(img_url[0])+"\n\n"+'剩余搜索次数 30s|24h: '+str(shortremain)+'|'+str(longremain)
                        # elif index_id ==34:
                        #     img_msg ="搜索平台："+service_name+"  相似度为"+str(similarity)+"[CQ:image,file="+str(min_img_url)+"]"+"PID:"+str(illust_id)+'剩余搜索次数 30s|24h: '+str(shortremain)+'|'+str(longremain)
                        elif index_id == 10:# or 11 or 8:
                            img_msg ="搜索平台："+service_name+"  相似度为"+str(similarity)+"[CQ:image,file="+str(min_img_url)+"]"+"PID:"+str(illust_id)+"\n"+"UID:"+str(member_id)+'剩余搜索次数 30s|24h: '+str(shortremain)+'|'+str(longremain)
                        # elif index_id == 9:
                        #     img_msg ="搜索平台："+service_name+"  相似度为"+str(similarity)+"[CQ:image,file="+str(min_img_url)+"]"+"PID:"+str(illust_id)+"\n"+"UID:"+str(member_id)+"\n"+"地址:\n\n"+str(img_url[0])+"\n\n"'剩余搜索次数 30s|24h: '+str(shortremain)+'|'+str(longremain)
                    return [processResults, img_msg]
                except Exception as e:
                    print("没有适配，开摆")
                    # print(e)
                    return [processResults,"没有适配呢，甩你个网址先\n"+str(results['results'][0]['data']['ext_urls'])]
            else:#匹配度不够
                print('miss... ' + str(results['results'][0]['header']['similarity']))
                return [processResults, "啊这，搜索结果相似度不够"]

        else:#没有搜索结果
            print('no results... ;_;')
            return [processResults, "啊这，没有搜索结果"]

    if not processResults:
        return [processResults, "啊这，未成功搜索"]

    if int(results['header']['long_remaining']) < 1:  # could potentially be negative
        print('Out of searches for today. Sleeping for 6 hours...')
        time.sleep(6 * 60 * 60)
    if int(results['header']['short_remaining']) < 1:
        print('Out of searches for this 30 second period. Sleeping for 25 seconds...')
        time.sleep(25)
    


    



