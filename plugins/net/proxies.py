import requests
import logging
#TODO: висит селери и парсит себе прокси, периодически проверяет и отдаёт рабочие по запросу
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

countries = ['AL', 'BS', 'DE', 'EG', 'SE', 'UA', 'US', 'NL', 'FR']

headers = {
    'User-Agent': 'curl/7.65.0',
    'Accept': '*/*'
}

NET_TIMEOUT = 10
ANON_LVL = 'anonymous'

def _get_proxy_list(proxy_type, country='US'):
    assert proxy_type in ['http', 'https'], f'{proxy_type} ещё не поддерживается' #, 'socks4', 'socks5']
    params = {
        'type': proxy_type,
        'anon': ANON_LVL,
        'country': country
    }
    logger.info(f'Country: {params["country"]}')
    logger.info(f'Type: {params["type"]}')
    url = 'https://www.proxy-list.download/api/v1/get/'
    req = requests.get(url, params=params)
    return req.text

def is_proxy_available(proxy, p_type):
    logger.info(f'Checking {proxy}')
    try:
        req = requests.get('https://2ip.ru', proxies={p_type: proxy}, headers=headers, timeout=NET_TIMEOUT)
    except:
        logger.error('Unavailable')
        return False
    result_ip = req.text.strip()
    #logger.debug(f'{result_ip} == {proxy.split(":")[0]}')
    if result_ip != proxy.split(':')[0] and ANON_LVL != 'transparent':
        logger.error("IP isn't changed")
        return False
    try:
        req = requests.get('https://lurkmore.to', proxies={p_type: proxy}, headers=headers, timeout=NET_TIMEOUT)
        return True
    except Exception as e: 
        logger.error("Still blocked" + str(e))
        return False

def _check_proxy_list(proxy_list, ptype):
    for p in proxy_list:
        try:
            if p != '' and is_proxy_available(p, ptype):
                return p
        except requests.exceptions.ProxyError:
            continue
    else:
        return False

def get_working_proxy(ptype, **kwargs):
    country_list = kwargs['countries'] if 'countries' in kwargs else countries
    for country in country_list:
        plist = _get_proxy_list(ptype, country=country).split('\r\n')[:-1]
        logger.info(f'Got list of {len(plist)} proxies')
        if len(plist) > 1:
            proxy = _check_proxy_list(plist, ptype)
            if proxy:
                return proxy
    return 'No proxies available now. Wait or extend countries list'

def start():
    print(get_working_proxy('https'))
    

if __name__ == '__main__':
    #print(is_proxy_available('13.52.154.16:3128', 'https'))
    print(get_working_proxy('https'))
