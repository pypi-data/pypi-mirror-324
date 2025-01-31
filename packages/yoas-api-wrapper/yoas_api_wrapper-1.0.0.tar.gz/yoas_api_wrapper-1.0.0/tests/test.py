from yoas_api_wrapper import YOASAPIWrapper, MessageCreate, UserCreate

api_server = "http://127.0.0.1:8001/api/yoas"
api = YOASAPIWrapper(api_server)
with open("../KEY", "r") as f:
    access_key = f.read().strip()

# create_user = api.create_user(
#     access_key=access_key,
#     user=UserCreateV1(
#         user_id=102,
#         message=MessageCreateV1(
#             text="Hello from wrapper"
#         ),
#         ban_reason="BAN REASON",
#         additional_info="ADDITIONAL INFO"
#     )
# )
#
# print("create_user:", create_user, end="\n\n")

# get_user = api.get_user(
#     user_id=102
# )
#
# print("get_user:", get_user, end="\n\n")
#
# get_message = api.get_message(
#     message_text="Hello from wrapper"
# )
#
# print("get_message:", get_message, end="\n\n")

# delete_user = api.delete_user(
#     access_key=access_key,
#     user_id=102
# )
#
# print("delete_user:", delete_user)

msg = """CРOЧHO!!CРOЧHO!!CРOЧHO!!
НУЖДАЕМСЯ В OТВЕТCТВЕHHЫХ ЛЮДЯХ
 (ВОЗРАСТ OТ 18)
OHЛАЙH СОТРУДНИЧЕСТВО, СТЕЙКИНГ
1-2 ЧАCА В ДЕHЬ -  900-1200$ в неделю
ОБРАЩАЙТЕСЬ В ЛИЧНЫЕ СООБЩЕНИЯ"""
test = api.get_message(msg)
print("test:", test)

test2 = api.get_user(6368526539)
print("test2:", test2)

text = "Как $300 стали $42,585?  Год назад Даниил и Сэм порекомендовали своим подписчикам 3 монеты:  REPE: $100 превратились в $16,280 APEX: $100 превратились в $11,105 AGI: $100 превратились в $15,200 Итог: $300 стали $42,585.  Это всего лишь 3 монеты из множества идей, которыми регулярно делятся Даниил и Сэм в своем канале Simple Money.  Сегодня вышел новый урок с актуальным списком монет и методикой закупки на 2024 год.  Успей узнать подробности, пока цены не ушли в космос.  Bcтупить"
test3 = api.get_message(text)
print("test3:", test3)

text2 = "Нужны люди. Есть пару мест. Дистанционная занятость,  стабильный высокий доход. Подробности в лс"
test4 = api.get_message(text2)
print("test4:", test4)

text3 = """﻿Κaκ $300 cтaли $42,585?

Γοд нaзaд Дaниил и Cэм дaли cвοим пοдпиcчиκaм 3 мοнeты:

RΕΡΕ: $100 ➜ $16,280
ΑΡΕΧ: $100 ➜ $11,105
ΑGΙ: $100 ➜ $15,200
Итοг: $300 cтaли $42,585.

И этο вceгο 3 мοнeты из мнοжecтвa идeй, κοтοpыми οни дeлятcя в cвοeм κaнaлe Simple Μοney.

Ceгοдня вышeл нοвый уpοκ c aκтуaльным cпиcκοм мοнeт и мeтοдиκοй зaκупκи нa 2024 гοд.

Узнaй пοдpοбнοcти, пοκa нe cтaлο пοзднο!

Bcтупить"""
test5 = api.get_message(text3)
print("test5:", test5)
