import requests
import json
import bs4
import random
import webbrowser

# Generates Adidas URL for sneaker based on sneaker type, size, and model
def URLGen(model,size):
    base_size = 560
    # this base size is for size 5.5 shoes
    shoe_size = size - 5.5
    shoe_size = shoe_size * 20
    raw_size = shoe_size + base_size
    shoe_size_code = int(raw_size)
    URL = 'https://www.adidas.com/us/nmd_r1/' + str(model) + '.html?forceSelSize=' + str(model) + '_' + str(shoe_size_code)
    return URL

# Returns a dictionary of shoes sizes and online availability
# for a specific Adidas sneaker model
def check_stock(model):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    size_url = 'https://www.adidas.com/api/products/' + str(model) + '/availability?sitePath=us'
    raw_sizes =  (requests.get(size_url,headers=headers)).text
    size_data =  json.dumps(json.loads(raw_sizes))
    list = size_data['variation_list']
    i = 0
    size_dict = {}
    size_lookup = {}
    keys = range(20)
    for k in keys:
        size_dict[i] = {list[i]['size']:list[i]['availability_status']}
        i=i+1
    for key,value in size_dict.items():
        size_lookup.update(value)
    return size_lookup

# Main method
def main(model, size):
    url = URLGen(model,size)
    check_stock(model)
