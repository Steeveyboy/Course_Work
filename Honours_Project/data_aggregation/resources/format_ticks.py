import json

def format_ticks(dict):
    new_dc = {}
    for entry in dict.values():
        new_dc[entry["ticker"]] = {"cik": entry['cik_str'], "title": entry["title"]}
    return new_dc

if __name__ == '__main__':
    
    unformatted =  json.load(open('tickers_unformatted.json', 'r'))
    new_ticks = format_ticks(dict(unformatted))
    
    with open('tickers.json', 'w') as file:
        file.write(json.dumps(new_ticks))


