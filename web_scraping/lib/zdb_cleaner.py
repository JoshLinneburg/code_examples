import ast
import json
from scraping_utils import output_exception
from scraping_utils import output_log


def clean_zdb():
    """
    Cleans the zdb.txt file used in the web scraping process and makes it into a
    properly-formatted JSON file.

    Returns
    -------
    None
    """
    float_fields = ['lat', 'lon']

    try:
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

    except:
        exc = sys.exc_info()
        exc_str = output_exception(exc=exc)
        output_log(filename='../logs/zdb_cleaner.log',
                   text=exc_str,
                   append=True)


if __name__ == '__main__':
    clean_zdb()
