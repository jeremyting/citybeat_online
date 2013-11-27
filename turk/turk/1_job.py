import jinja2, pymongo

def connect_mongo(db_name,collection_name):
    conn = pymongo.Connection()
    conn["admin"].authenticate('admin','mediumdatarules')
    db = conn[db_name]
    collection = db[collection_name]
    return collection

def main():
    collection = connect_mongo("citybeat_production","instagram_frontend_events")
    photo_urls = []
    for event in collection.find({"mechanical_turk_label":-100},timeout=False):
        _id = event["_id"]
        #collection.update({"_id":_id},{$set:{"mechanical_turk_label":100}}) ## Set to marked
        for capture in event["photos"]:
            photo_urls.append(capture["images"]["standard_resolution"])

        env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        html = env.get_template('1_start_template.html').render(photo_urls=photo_urls)
        o = open("job1.html",'w')
        o.write(html)
        o.close()
def test():
    urls = [["http://distilleryimage9.s3.amazonaws.com/dc7aaa5c422a11e3880f22000a1f9ca7_8.jpg","http://distilleryimage9.s3.amazonaws.com/dc7aaa5c422a11e3880f22000a1f9ca7_8.jpg","http://distilleryimage9.s3.amazonaws.com/dc7aaa5c422a11e3880f22000a1f9ca7_8.jpg","http://distilleryimage9.s3.amazonaws.com/dc7aaa5c422a11e3880f22000a1f9ca7_8.jpg"],
          ["http://distilleryimage10.s3.amazonaws.com/8b1aabd4422b11e3a34e22000ae91355_7.jpg","http://distilleryimage10.s3.amazonaws.com/8b1aabd4422b11e3a34e22000ae91355_7.jpg","http://distilleryimage10.s3.amazonaws.com/8b1aabd4422b11e3a34e22000ae91355_7.jpg","http://distilleryimage10.s3.amazonaws.com/8b1aabd4422b11e3a34e22000ae91355_7.jpg"],
          ["http://distilleryimage1.s3.amazonaws.com/a0594eba422b11e3bb5722000aeb3e27_8.jpg","http://distilleryimage1.s3.amazonaws.com/a0594eba422b11e3bb5722000aeb3e27_8.jpg","http://distilleryimage1.s3.amazonaws.com/a0594eba422b11e3bb5722000aeb3e27_8.jpg","http://distilleryimage1.s3.amazonaws.com/a0594eba422b11e3bb5722000aeb3e27_8.jpg"],
          ["http://distilleryimage9.s3.amazonaws.com/1b6b677c411511e3a86c22000ae81daf_8.jpg","http://distilleryimage9.s3.amazonaws.com/1b6b677c411511e3a86c22000ae81daf_8.jpg","http://distilleryimage9.s3.amazonaws.com/1b6b677c411511e3a86c22000ae81daf_8.jpg","http://distilleryimage9.s3.amazonaws.com/1b6b677c411511e3a86c22000ae81daf_8.jpg"],
          ["http://distilleryimage11.s3.amazonaws.com/a2ddbb16411411e39a9c22000a1fbe09_8.jpg","http://distilleryimage11.s3.amazonaws.com/a2ddbb16411411e39a9c22000a1fbe09_8.jpg","http://distilleryimage11.s3.amazonaws.com/a2ddbb16411411e39a9c22000a1fbe09_8.jpg","http://distilleryimage11.s3.amazonaws.com/a2ddbb16411411e39a9c22000a1fbe09_8.jpg"]]
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    html = env.get_template('1_start_template.html').render(photo_urls=urls)
    o = open("index1.html",'w')
    o.write(html)
    o.close()
test()
