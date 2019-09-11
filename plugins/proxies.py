from . import WPlugin
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import logging
#TODO: висит селери и парсит себе прокси, периодически проверяет и отдаёт рабочие по запросу
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class WProxies(WPlugin):

    TRANSPARENT = 'transparent'
    ANON = 'anonymous'

    def __init__(self):
        self.cfg = {}
        self.config()

    def config(self, **kwargs):
        self.cfg.clear()
        defaults = {
            'countries': ['AL', 'BS', 'DE', 'EG', 'SE', 'UA', 'US', 'NL', 'FR'],
            'headers': {
                'User-Agent': 'curl/7.65.0',
                'Accept': '*/*'
            },
            'net_timeout': 4,
            'max_workers': 50,
            'anon_lvl': WProxies.ANON,
            'proxy_type': 'https'
        }

        for k,v in defaults.items():
            if k in kwargs:
                v = kwargs[k]
            self.cfg[k] = v

    def _get_proxy_list(self, proxy_type, country):
        assert proxy_type in ['http', 'https'], f'{proxy_type} ещё не поддерживается' #, 'socks4', 'socks5']
        params = {
            'type': proxy_type,
            'anon': self.cfg['anon_lvl'],
            'country': country
        }
        url = 'https://www.proxy-list.download/api/v1/get/'
        logger.info(f'Country: {params["country"]}, {params["type"]}')
        req = requests.get(url, params=params)
        return req.text

    def is_proxy_available(self, proxy, p_type):
        logger.info(f'Checking {proxy}')
        try:
            req = requests.get('https://2ip.ru', proxies={p_type: proxy}, headers=self.cfg['headers'], timeout=self.cfg['net_timeout'])
        except:
            logger.error(f'{p_type}://{proxy} is unavailable')
            return 0
        result_ip = req.text.strip()
        #logger.debug(f'{result_ip} == {proxy.split(":")[0]}')
        if result_ip != proxy.split(':')[0] and self.cfg['anon_lvl'] != WProxies.TRANSPARENT:
            logger.error(f"{p_type}://{proxy} doesn't change IP")
            return 0
        try:
            req = requests.get('https://lurkmore.to', proxies={p_type: proxy}, headers=self.cfg['headers'], timeout=self.cfg['net_timeout'])
            elapsed = req.elapsed.total_seconds()
            logger.info(f'{proxy} -> {elapsed} s.')
            return elapsed
        except Exception: 
            logger.error(f'{p_type}://{proxy} is still blocked')
            return 0

    def _check_proxy_list(self, proxy_list, proxy_type):
        min_elapsed_time = float('inf')
        best_proxy = None
        with ThreadPoolExecutor(max_workers=self.cfg['max_workers']) as pool:
            futures = {pool.submit(self.is_proxy_available, proxy_addr, proxy_type): proxy_addr
                        for proxy_addr in proxy_list if proxy_addr != ''}
            for future in as_completed(futures):
                try:
                    elapsed = future.result()
                except requests.exceptions.ProxyError:
                    continue
                if 0 < elapsed < min_elapsed_time:
                    min_elapsed_time = elapsed
                    best_proxy = futures[future]
        return best_proxy, min_elapsed_time

    def process(self, **kwargs):
        self.config(**kwargs)
        proxies = []
        logger.info(f"Search countries: {self.cfg['countries']}")
        try:
            for country in self.cfg['countries']:
                plist = self._get_proxy_list(self.cfg['proxy_type'], country=country).split('\r\n')[:-1]
                logger.info(f'Got list of {len(plist)} proxies')
                if len(plist) > 1:
                    proxy = self._check_proxy_list(plist, self.cfg['proxy_type']) # подрубить асинхроночки и отдавать самый шустрый прокси
                    if proxy[0]:
                        proxies.append(proxy + (country,))
        except KeyboardInterrupt:
            return proxies
        return proxies if proxies else ('No proxies available now. Wait or extend countries list',)
