Помощник для моей системы, (ибо искать готовые решения лень), который:
* может отслеживать мои репозитории на незакоммиченность -
* будет собирать прохождения лаб на хтб и рутме, искать незаконченные  -
* будет показывать мои текущие задачи, которые я не выполню (красная цифорка над кнопкой)  -
* висит в трее - 
* декодирует всякую хрень, типа rot13 и urlencoded-строки +  
* будет собирать все неактивные вкладки из браузера -
* имеет шифрованное хранилище, содержащее код самой проги -
* ищет !рабочие! прокси (в т.ч. MTproto) +
* интегрируется с телегой -
* парсит ольбомы с комментариями (вероятно в другом проекте) -
* производит мониторинг процессов и суспенд самых наглых при исчерпании всей памяти -
* умеет пускать весь трафик через тор -
* запускает задачи в отдельных процессах +
* общается с процессами через unix-sockets
* бэкапит систему в виде списка установленных пакетов и конфигов (локальных + глобальных) +
* какая-то хрень наподобие sftp с возможностью качать/загружать файлы (но скорей всего будет обёрткой над ssh) -
* обладает соей версией goodbyeDPI -
* будет автоматически подниматься (ограниченное кол-во попыток) при падении (внезапном и не наступившем сразу после запуска) -
* каждый процесс отслеживает себя на запущенность через сокет, если пытаюсь запустить новый, то он будет переадресовывать по api (flask?) исходному
