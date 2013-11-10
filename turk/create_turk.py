from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion,QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer

ACCESS_KEY = 'AKIAIQ3NNF7F7GTVRASA' ##read from s3?
SECRET_KEY = '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'
SANDBOX = 'mechanicalturk.sandbox.amazonaws.com'

mtc = MTurkConnection(aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY,
                      host=SANDBOX)

title = 'Give your opinion about a website'
description = ('Visit a website and give us your opinion about'
               ' the design and also some personal comments')
keywords = 'website, rating, opinions'



#--------------- BUILD THE QUESTION FORM -------------------
question_form = ExternalQuestion("https://s3-us-west-2.amazonaws.com/turk-html/test.html",500)


#--------------- CREATE THE HIT -------------------

mtc.create_hit(question=question_form,
               max_assignments=1,
               title=title,
               description=description,
               keywords=keywords,
               duration = 60*5,
               reward=0.05)

