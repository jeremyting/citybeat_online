import jinja2

def write_jinja(template,image_urls):
	env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
	html = env.get_template(template).render(photo_urls=image_urls)
	o = open("second_stage.html",'w')
	o.write(html)
	o.close()

def main(image_urls,job1_results):
		if job1_results[0] is "yes": #Is an emergency
			write_jinja('2a_emer_template.html',image_urls)
		elif job1_results[0] is "no":
			write_jinja('2b_reg_template.html',image_urls)

urls = [["http://distilleryimage9.s3.amazonaws.com/dc7aaa5c422a11e3880f22000a1f9ca7_8.jpg","http://distilleryimage9.s3.amazonaws.com/dc7aaa5c422a11e3880f22000a1f9ca7_8.jpg","http://distilleryimage9.s3.amazonaws.com/dc7aaa5c422a11e3880f22000a1f9ca7_8.jpg","http://distilleryimage9.s3.amazonaws.com/dc7aaa5c422a11e3880f22000a1f9ca7_8.jpg"],
		  ["http://distilleryimage10.s3.amazonaws.com/8b1aabd4422b11e3a34e22000ae91355_7.jpg","http://distilleryimage10.s3.amazonaws.com/8b1aabd4422b11e3a34e22000ae91355_7.jpg","http://distilleryimage10.s3.amazonaws.com/8b1aabd4422b11e3a34e22000ae91355_7.jpg","http://distilleryimage10.s3.amazonaws.com/8b1aabd4422b11e3a34e22000ae91355_7.jpg"],
		  ["http://distilleryimage1.s3.amazonaws.com/a0594eba422b11e3bb5722000aeb3e27_8.jpg","http://distilleryimage1.s3.amazonaws.com/a0594eba422b11e3bb5722000aeb3e27_8.jpg","http://distilleryimage1.s3.amazonaws.com/a0594eba422b11e3bb5722000aeb3e27_8.jpg","http://distilleryimage1.s3.amazonaws.com/a0594eba422b11e3bb5722000aeb3e27_8.jpg"],
		  ["http://distilleryimage9.s3.amazonaws.com/1b6b677c411511e3a86c22000ae81daf_8.jpg","http://distilleryimage9.s3.amazonaws.com/1b6b677c411511e3a86c22000ae81daf_8.jpg","http://distilleryimage9.s3.amazonaws.com/1b6b677c411511e3a86c22000ae81daf_8.jpg","http://distilleryimage9.s3.amazonaws.com/1b6b677c411511e3a86c22000ae81daf_8.jpg"],
		  ["http://distilleryimage11.s3.amazonaws.com/a2ddbb16411411e39a9c22000a1fbe09_8.jpg","http://distilleryimage11.s3.amazonaws.com/a2ddbb16411411e39a9c22000a1fbe09_8.jpg","http://distilleryimage11.s3.amazonaws.com/a2ddbb16411411e39a9c22000a1fbe09_8.jpg","http://distilleryimage11.s3.amazonaws.com/a2ddbb16411411e39a9c22000a1fbe09_8.jpg"]]
main(urls,["yes"])
