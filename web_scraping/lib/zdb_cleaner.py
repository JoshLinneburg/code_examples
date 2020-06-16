import ast
import json

float_fields = ['lat', 'lon']

with open('../data/input/zdb.txt', 'r+') as f:
    raw_data = f.read()
    f.close()
    zdb = ast.literal_eval(raw_data)

    for d in zdb:
        for key, value in d.items():
            if key in float_fields:
                d[key] = float(value)
            else:
                d[key] = str(value)

with open('../data/input/geo_data.json', 'w+', encoding='UTF-8') as writer:
    json.dump(obj=zdb, fp=writer, ensure_ascii=True, indent=4)