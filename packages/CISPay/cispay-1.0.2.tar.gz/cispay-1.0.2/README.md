# PythonLib
> Библиотека, разработанная для Python 3.7+, которая позволяет создавать платежи и проверять их статус

---
#### Инструкция
##### Установка библиотеки
- 1.1. Выполните команду - `pip install CISPay`
или
- 1.2. Скачайте исходный код - `git clone https://github.com/CISPay/PythonLib`

#### Использование
##### Создание счета
```
from CISPay import CISPay

client = CISPay('uuid') # UUID вашего мерчанта

amount = 500
comment = 'Test'
expire = 1500

data = client.order_create(amount, comment, expire)
# data = {
#    'status': 'success', 
#    'uuid': 'a3938999-155b-42ba-9e48-9fd0a8a8dc77', 
#    'url': 'https://acquire.cispay.pro/a3938999-155b-42ba-9e48-9fd0a8a8dc77', 
#    'expire': 1685566800, 
#    'sum': 500.0 
# }
```
##### Получение информации о счете
```
from CISPay import CISPay

client = CISPay('uuid') # UUID вашего мерчанта
uuid = 'a3938999-155b-42ba-9e48-9fd0a8a8dc77' # Полученный UUID при создании счета

data = client.order_info(uuid)
# data = {
#    'status': 'success', 
#    'id': 123,
#    'uuid': 'a3938999-155b-42ba-9e48-9fd0a8a8dc77', 
#    'shop_uuid': 'dc4bc78f-27ba-4778-96ce-905c6b23c3e9',
#    'amount': 500.0,
#    'comment': 'Test',
#    'expire': 1685566800, 
#    'is_test': 1
# }
```
---

## Лицензия

Copyright © 2025 [CISPay](https://github.com/CISPay)

Проект распространяется под лицензией [MIT](LICENSE)
