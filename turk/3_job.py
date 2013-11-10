import jinja2

def main(image_urls):
	env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
	html = env.get_template("3_select_template.html").render(photo_urls=image_urls)
	o = open("third.html",'w')
	o.write(html)
	o.close()

urls = [["http://distilleryimage9.s3.amazonaws.com/dc7aaa5c422a11e3880f22000a1f9ca7_8.jpg","http://distilleryimage9.s3.amazonaws.com/dc7aaa5c422a11e3880f22000a1f9ca7_8.jpg","http://distilleryimage9.s3.amazonaws.com/dc7aaa5c422a11e3880f22000a1f9ca7_8.jpg","http://distilleryimage9.s3.amazonaws.com/dc7aaa5c422a11e3880f22000a1f9ca7_8.jpg"],
		  ["http://distilleryimage10.s3.amazonaws.com/8b1aabd4422b11e3a34e22000ae91355_7.jpg","http://distilleryimage10.s3.amazonaws.com/8b1aabd4422b11e3a34e22000ae91355_7.jpg","http://distilleryimage10.s3.amazonaws.com/8b1aabd4422b11e3a34e22000ae91355_7.jpg","http://distilleryimage10.s3.amazonaws.com/8b1aabd4422b11e3a34e22000ae91355_7.jpg"],
		  ["http://distilleryimage1.s3.amazonaws.com/a0594eba422b11e3bb5722000aeb3e27_8.jpg","http://distilleryimage1.s3.amazonaws.com/a0594eba422b11e3bb5722000aeb3e27_8.jpg","http://distilleryimage1.s3.amazonaws.com/a0594eba422b11e3bb5722000aeb3e27_8.jpg","http://distilleryimage1.s3.amazonaws.com/a0594eba422b11e3bb5722000aeb3e27_8.jpg"],
		  ["http://distilleryimage9.s3.amazonaws.com/1b6b677c411511e3a86c22000ae81daf_8.jpg","http://distilleryimage9.s3.amazonaws.com/1b6b677c411511e3a86c22000ae81daf_8.jpg","http://distilleryimage9.s3.amazonaws.com/1b6b677c411511e3a86c22000ae81daf_8.jpg","http://distilleryimage9.s3.amazonaws.com/1b6b677c411511e3a86c22000ae81daf_8.jpg"],
		  ["http://distilleryimage11.s3.amazonaws.com/a2ddbb16411411e39a9c22000a1fbe09_8.jpg","http://distilleryimage11.s3.amazonaws.com/a2ddbb16411411e39a9c22000a1fbe09_8.jpg","http://distilleryimage11.s3.amazonaws.com/a2ddbb16411411e39a9c22000a1fbe09_8.jpg","http://distilleryimage11.s3.amazonaws.com/a2ddbb16411411e39a9c22000a1fbe09_8.jpg"]]

main(urls)