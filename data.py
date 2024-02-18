from datetime import date, timedelta


def get(array):
    incomes, expenses, incomes_categories, expenses_categories = {}, {}, {}, {}
    for i in range(len(array)):
        if array[i][1] == "Доход":
            if array[i][2] in incomes_categories.keys():
                incomes_categories[array[i][2]] += float(array[i][4])
            else:
                incomes_categories[array[i][2]] = float(array[i][4])
            if array[i][0] in incomes.keys():
                incomes[array[i][0]] += float(array[i][4])
            else:
                incomes[array[i][0]] = float(array[i][4])
        elif array[i][1] == "Расходы":
            if array[i][2] in expenses_categories.keys():
                expenses_categories[array[i][2]] += float(array[i][4])
            else:
                expenses_categories[array[i][2]] = float(array[i][4])
            if array[i][0] in expenses.keys():
                expenses[array[i][0]] += float(array[i][4])
            else:
                expenses[array[i][0]] = float(array[i][4])
    return incomes_categories, expenses_categories, dict(sorted(incomes.items())), dict(sorted(expenses.items()))


def stats(incomes_categories, expenses_categories, incomes, expenses):
    maxkeys1 = sorted(incomes_categories, key=incomes_categories.get)[:-5:-1]
    maxkeys2 = sorted(expenses_categories, key=expenses_categories.get)[:-5:-1]
    maxvalues1 = sorted(incomes_categories.values())[:-5:-1]
    maxvalues2 = sorted(expenses_categories.values())[:-5:-1]
    text1, text2, sum1, sum2 = "", "", 0, 0
    if maxkeys1:
        text1 += f"Топ {len(maxkeys1)} категории с максимальными доходами:\n"
        for i in range(len(maxkeys1)):
            text1 += f"{i+1}. {maxkeys1[i]} ({'{:,.2f}'.format(maxvalues1[i])} руб.)\n"
    if maxkeys2:
        if maxkeys1:
            text1 += "\n"
        text1 += f"Топ {len(maxkeys2)} категории с максимальными расходами:\n"
        for j in range(len(maxkeys2)):
            text1 += f"{j+1}. {maxkeys2[j]} ({'{:,.2f}'.format(maxvalues2[j])} руб.)\n"
    dates1, sums1 = [date(*list(map(int, key.split("-")))) for key in incomes.keys()], list(incomes.values())
    dates2, sums2 = [date(*list(map(int, key.split("-")))) for key in expenses.keys()], list(expenses.values())
    date_now = date.today()-timedelta(days=31)
    if dates1:
        for i in range(len(dates1)-1, -1, -1):
            if dates1[i] > date_now:
                sum1 += sums1[i]
    if dates2:
        for j in range(len(dates2)-1, -1, -1):
            if dates2[j] > date_now:
                sum2 += sums2[j]
    text2 += f"За последние 30 дней заработано: {'{:,.2f}'.format(sum1)} руб.\n"
    text2 += f"За последние 30 дней потрачено: {'{:,.2f}'.format(sum2)} руб.\n"
    text2 += f"Чистая прибыль составляет: {'{:,.2f}'.format(sum1-sum2)} руб.\n"
    if sum1-sum2 <= 0:
        text2 += f"Ваша прибыль отрицательная.\n\nРекомендуем снизить свои расходы или начать зарабатывать больше."
    elif sum1-sum2*2 <= 0:
        text2 += f"Вы расходуете больше половины ваших доходов.\n\nРекомендуем немного снизить свои расходы."
    elif sum1-sum2*3 <= 0:
        text2 += f"Вы имеете стабильную прибыль.\n\nПредлагаем вложить 10% своих доходов в банк под проценты."
    else:
        text2 += f"Вы имеете стабильную прибыль.\n\nПредлагаем вложить 30% своих доходов в ценные бумаги или в банк под проценты."
    return text1, text2


def save(array):
    dates, types, category, comments, sums = [], [], [], [], []
    for i in array:
        dates.append(date(*list(map(int, i[0].split("-")))))
        types.append(i[1])
        category.append(i[2])
        comments.append(i[3])
        sums.append(float(i[4]))
    return {"Дата": dates, "Тип": types, "Категория": category, "Комментарии": comments, "Сумма (в рублях)": sums}


def load(array):
    dates, types, category, comments, sums = [], [], [], [], []
    try:
        for i in range(len(array["Дата"])):
            if f"{array["Дата"][i]}" != "NaT":
                dates.append(array["Дата"][i].date())
            else:
                return "Не все ячейки в столбце 'Дата' заполнены!"
    except Exception as er:
        if type(er) == KeyError:
            return f"В импортируемом файле отсутствует столбец {er}!"
        elif type(er) == AttributeError:
            return "Неверный формат даты!\nПравильно: dd.mm.yyyy"
        else:
            return f"{er.__class__.__name__}: {er}.\nСообщите разработчикам об ошибке."
    try:
        for i in range(len(array["Тип"])):
            if array["Тип"][i] in ["Доход", "Расходы"]:
                if array["Тип"][i] == "Доход" and array["Категория"][i] in \
                        ["Работа/Подработка", "Пенсия", "Проценты по вкладам", "Дивиденды",
                         "Рента", "Соц.выплаты/Пособия", "Вознаграждение", "Подарки", "Другое"] or \
                   array["Тип"][i] == "Расходы" and array["Категория"][i] in \
                        ["Налоги", "Кредит", "Аренда/Съём", "ЖКУ", "Продукты питания",
                         "Одежда и обувь", "Здравоохранение", "Образование", "Транспорт",
                         "Бытовая техника", "Электроника", "Машина", "Недвижимость",
                         "Предметы роскоши", "Хобби и отдых", "Внезапные расходы", "Другое"]:
                    types.append(array["Тип"][i])
                    category.append(array["Категория"][i])
                elif array["Тип"][i] == "Доход" and f"{array["Категория"][i]}" != "nan":
                    return ("У типа 'Доход' присутствует неизвестная категория!\n"
                            "Правильно: 'Работа/Подработка', 'Пенсия', 'Проценты по вкладам', 'Дивиденды', "
                            "'Рента', 'Соц.выплаты/Пособия', 'Вознаграждение', 'Подарки' или 'Другое'.")
                elif array["Тип"][i] == "Расходы" and f"{array["Категория"][i]}" != "nan":
                    return ("У типа 'Расходы' присутствует неизвестная категория!\n"
                            "Правильно: 'Налоги', 'Кредит', 'Аренда/Съём', 'ЖКУ', 'Продукты питания', "
                            "'Одежда и обувь', 'Здравоохранение', 'Образование', 'Транспорт', 'Бытовая техника', "
                            "'Электроника', 'Машина', 'Недвижимость', 'Предметы роскоши', 'Хобби и отдых', "
                            "'Внезапные расходы' или 'Другое'.")
                else:
                    return "Не все ячейки в столбце 'Категория' заполнены!"
            elif f"{array["Тип"][i]}" != "nan":
                return "Присутствует неизвестный тип!\nПравильно: 'Доход' или 'Расходы'."
            else:
                return "Не все ячейки в столбце 'Тип' заполнены!"
    except Exception as er:
        if type(er) == KeyError:
            return f"В импортируемом файле отсутствует столбец {er}!"
        else:
            return f"{er.__class__.__name__}: {er}.\nСообщите разработчикам об ошибке."
    try:
        for i in range(len(array["Сумма (в рублях)"])):
            if f"{array["Сумма (в рублях)"][i]}" != "nan":
                sums.append("%.2f" % float(array["Сумма (в рублях)"][i]))
            else:
                return "Не все ячейки в столбце 'Сумма (в рублях)' заполнены!"
        sums = list(map(float, sums))
    except Exception as er:
        if type(er) == KeyError:
            return f"В импортируемом файле отсутствует столбец {er}!"
        elif type(er) == ValueError:
            return f"В столбце 'Сумма (в рублях)' должны быть числа!"
        else:
            return f"{er.__class__.__name__}: {er}.\nСообщите разработчикам об ошибке."
    if "Комментарии" in array.columns.ravel():
        for i in range(len(array["Комментарии"])):
            if f"{array["Комментарии"][i]}" != "nan":
                comments.append(array["Комментарии"][i])
            else:
                comments.append("")
    return [dates, types, category, comments, sums]
