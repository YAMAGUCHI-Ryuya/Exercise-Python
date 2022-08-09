items = {"eracer": [100, 2], "pen": [200, 3], "notebook": [400, 5]}
total_price = 0

for item in items:
    print(item + "は1個" + str(items[item][0]) + "円で" + str(items[item][1]) + "個購入します")
    total_price = items[item][0] * items[item][1]

    print("支払い金額は" + str(total_price) + "円です")

    money = 2000

    if money > total_price:
        print("お釣りは" + str(money - total_price) + "です")
    elif money == total_price:
        print("お釣りはありません")
    else:
        print("お金が足りません")