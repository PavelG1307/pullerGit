#URL Shortener
---
1. Алгоритм создания ключа:
  a. Отправляется запрос на добавление, при этом поле url теперь с параметром unique, что не даст добавить второй такой же URL. Забирается «last rowid».
  b. Если данный URL уже был встречался ранее, программа делает запрос в БД и получает rowid.
  с. При помощи алгоритма MD5 хэшируем id и передаем его в качестве ключа обратно.

3. Алгоритм перехода по ключу:
  a. После получения ключа, идет запрос в кэш, если там есть такой ключ, то обратно сразу выдается url (а данная пара key - url переносится на первое место).
  b. Если в кэше нет такого ключа, ключ дешифруется
  c. Из БД запрашивается url с индексом, полученным при дешифровании.
  d. Если получили url, отправляем его обратно, в противном случае отправляем ответ со статусом 404.

3. Дальнейшее развитие:
  a. Многопоточность или ассинхроность
  b. Страница для добавления нового URL
  c. Личный кабинет, где пользователь мог бы делать свои собственные сокращеные ссылки
  d. Ограничил бы время действия короткой ссылки, чтобы не перегружать программу.
  e. Личный кабинет администратора ресурса (Для мониторинга за нагрузкой и количеством ссылок)

---
