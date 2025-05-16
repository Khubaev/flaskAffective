import json

from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSON_UTF-8'] = True
@app.route('/best_combinations', methods=['POST'])
def get_best_combinations():
    materials = request.json
    target_efficiency = materials["target_efficiency"]
    monthly_income = materials["monthly_income"]
    total = materials["total"]
    max_months = materials["max_months"]

    combinations = []
    # Генерация всех комбинаций
    for roof_material, roof_info in materials["КрышаИЧердак"].items():
        for basement_material, basement_info in materials["ПодвальныеПомещения"].items():
            for facade_material, facade_info in materials["Фасад"].items():
                combination = {
                    "КрышаИЧердак": {
                        "материал": roof_material,
                        "снижение": roof_info["снижение"],
                        "затраты": roof_info["затраты"]
                    },
                    "ПодвальныеПомещения": {
                        "материал": basement_material,
                        "снижение": basement_info["снижение"],
                        "затраты": basement_info["затраты"]
                    },
                    "Фасад": {
                        "материал": facade_material,
                        "снижение": facade_info["снижение"],
                        "затраты": facade_info["затраты"]
                    },
                    "ОбщееСнижение": roof_info["снижение"] + basement_info["снижение"] + facade_info["снижение"]
                }
                combinations.append(combination)

    filtered_combinations = [combo for combo in combinations if combo["ОбщееСнижение"] >= target_efficiency]

    # Сортировка отфильтрованных комбинаций по общему снижению в порядке убывания
    sorted_combinations = sorted(filtered_combinations, key=lambda x: x["ОбщееСнижение"], reverse=True)
    chosen_m = {}
    chosen_n = {}
    # Динамическое программирование для подсчета максимального снижения
    dp = [0] * (max_months + 1)
    dpcount = [0] * (max_months + 1)

    alldp = []
    allDp = []
    truminus = False

    for combo in sorted_combinations:
        alldp.append(chosen_m)
        allDp.append(dp)
        dp = [0] * (max_months + 1)
        dpcount = [0] * (max_months + 1)
        chosen_m = {}
        chosen_n = {}
        chosen_n["снижение"] = 0
        chosen_n["затраты"] = 0
        chosen_n["ИтогиПоденьгам"] = 0
        chosen_m["ОбщийИтог"] = chosen_n
        chosen_m["ОбщийМесяц"] = 0
        target = target_efficiency
        if max_months > 0:
            for month in range(1, max_months + 1):
                if target <= chosen_n["снижение"]:
                    break

                truminus = False

                for k, v in combo.items():
                    if k == "ОбщееСнижение":
                        continue
                    if truminus == True:
                        break
                    else:
                        if dp[month - 1] >= v['затраты']:
                            if chosen_m.get(k):
                                continue
                            else:
                                dp[month] = dp[month - 1] - v['затраты']
                                truminus = True
                                dpcount[month] = dpcount[month] + v['снижение']
                                dpcount = [dpcount[month]] * (max_months + 1)
                                d = {}
                                chosen_m[k] = d

                                chosen_m[k]["Материал"] = v['материал']
                                chosen_m[k]["Затраты"] = v['затраты']
                                chosen_m[k]["Снижение"] = v['снижение']
                                chosen_m["ОбщийИтог"]["снижение"] = chosen_n["снижение"] + v['снижение']
                                chosen_m["ОбщийИтог"]["затраты"] = chosen_n["затраты"] + v['затраты']
                                chosen_n["ИтогиПоДеньгам"] = dp[month]
                                chosen_m["ОбщийМесяц"] = month
                        else:
                            dp[month] = dp[month - 1] + monthly_income + (total  * dpcount[month] / 100)
                            dpcount[month] = dpcount[month]
                            chosen_n["ИтогиПоДеньгам"] = dp[month]
                            chosen_m["ОбщийМесяц"] = month
            chosen_m["ОбщийМесяц"] = month
        else:
            totalmouth = 0
            max_months = 0
            chosen_m["ОбщийМесяц"] = 0
            target = target_efficiency
            while target >= 0:
                if target_efficiency <= chosen_n["снижение"]:
                    break
                truminus = False

                for k, v in combo.items():
                    if k == "ОбщееСнижение":
                        continue
                    if truminus == True:
                        break
                    else:
                        if dp[max_months - 1] >= v['затраты']:
                            if chosen_m.get(k):
                                continue
                            else:
                                dp[max_months] = dp[max_months - 1] - v['затраты']
                                truminus = True
                                dpcount[max_months] = dpcount[max_months] + v['снижение']
                                dpcount = [dpcount[max_months]] * (max_months + 1)
                                d = {}
                                chosen_m[k] = d

                                chosen_m[k]["Материал"] = v['материал']
                                chosen_m[k]["Затраты"] = v['затраты']
                                chosen_m[k]["Снижение"] = v['снижение']
                                chosen_m["ОбщийИтог"]["снижение"] = chosen_n["снижение"] + v['снижение']
                                chosen_m["ОбщийИтог"]["затраты"] = chosen_n["затраты"] + v['затраты']
                                target = chosen_n["снижение"]
                                chosen_n["ИтогиПоДеньгам"] = dp[max_months]
                                totalmouth = totalmouth + 1
                                max_months = max_months + 1
                                dp.append(max(dpcount))
                                dpcount.append(max(dpcount))
                                chosen_m["ОбщийМесяц"] = totalmouth
                        else:
                            dp[max_months] = dp[max_months - 1] + monthly_income + (total * dpcount[max_months] / 100)
                            dpcount[max_months] = dpcount[max_months]
                            chosen_n["ИтогиПоДеньгам"] = dp[max_months]
                            totalmouth = totalmouth + 1
                            max_months = max_months + 1
                            dp.append(max(dpcount))
                            dpcount.append(max(dpcount))
                            chosen_m["ОбщийМесяц"] = totalmouth
            max_months = 0


    json_response = json.dumps(alldp, ensure_ascii=False)

    return json_response

if __name__ == '__main__':
    app.run(debug=True)