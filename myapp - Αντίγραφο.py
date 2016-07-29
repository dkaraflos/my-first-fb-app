from flask import Flask
from flask import request
import facebook
import requests
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask import render_template
import os
from flask import Markup
from contextlib import suppress
from collections import defaultdict
import operator



global number

number=2

app = Flask(__name__)
global y
y=0
graph1={'photo':0,'video':0,'link':0,'status':0,'offer':0,'note':0}
@app.route('/')
def index():
   
    return  render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    
    site = request.form['text']

    #site=site.replace("/", " ")
    
    #site = 'https://www.facebook.com/Merenda.gr/?fref=ts'
    token = 'EAAY6D3T4mz0BACVbtl3GjZCtI9ZBB9sBHjNqdjcdQ6O6UZCJ1ZAz73s6V07V4ojz8p4MBEAUfJ7K6rOUPGMFxdXeidZCZAYwfwPrfwojTVhoeEzMbgF1iwQBWA7QEfgGTw0JwNSVTf13mKnZAl9SgYWqyjTAI9CAyUZD'
    graph = facebook.GraphAPI(token)
    newstr = site.replace("https://www.facebook.com/", "")
    newstr = newstr.replace("/?fref=ts", "")
    p = graph.get_object(newstr)
    uid = p['id']
##
    show = graph.get_object(uid + '/insights/page_fans_country')
##
    coun = show['data'][0]['values'][0]['value']
    data={}
    shares={}
    words={}
    posts=graph.get_object(uid+'/posts?fields=created_time,type&limit=100')['data']
    
    for i in range(0,number):
            posts[i]['p_id']=posts[i]['id']
            del posts[i]['id']
            temp=graph.get_object(posts[i]['p_id']+'?fields=likes.summary(true).limit(0),comments.summary(true).limit(0),insights&limit=100')
            likes=temp['likes']['summary']
            likes['likes_count']=likes['total_count']
            del likes['total_count']
            comments=temp['comments']['summary']
            comments['comments_count']=comments['total_count']
            del comments['total_count']
            temp2=graph.get_object(posts[i]['p_id']+'?fields=shares,message')
            with suppress(Exception): # or, better, a more specific error (or errors)
                    shares=temp2['shares']
            if 'count' not in shares.keys(): shares['count']=0
            shares['shares_count']=shares['count']
            del shares['count']
            words['message']=temp2['message']
            

            
            data[i]={**posts[i],**likes,**comments,**shares,**words}

    
    tgraph={}
    textgraph={}
    for i in range(0,number):
            if data[i]['type']=='photo':
                    graph1['photo']=graph1['photo']+1
                    tgraph[i]={'type':'photo','message':data[i]['message']}
            elif data[i]['type']=='video':
                    graph1['video']=graph1['video']+1
                    tgraph[i]={'type':'video','message':data[i]['message']}
            elif data[i]['type']=='link':
                    graph1['link']=graph1['link']+1
                    tgraph[i]={'type':'link','message':data[i]['message']}
            elif data[i]['type']=='status':
                    graph1['status']=graph1['status']+1
                    tgraph[i]={'type':'status','message':data[i]['message']}
            elif data[i]['type']=='offer':
                    graph1['offer']=graph1['offer']+1
                    tgraph[i]={'type':'offer','message':data[i]['message']}
            elif data[i]['type']=='note':
                    graph1['note']=graph1['note']+1
                    tgraph[i]={'type':'note','message':data[i]['message']}
  

                    

    return str(graph1)

@app.route('/chart/', methods=['GET','POST'])
def chart(chartID = 'chart_ID', chart_type = 'bar', chart_height = 350):
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Label1', "data": [graph1['photo'],graph1['video'],graph1['link']]}]
	title = {"text": 'My Title'}
	xAxis = {"categories": ['photo', 'video', 'link']}
	yAxis = {"title": {"text": 'yAxis Label'}}
	return render_template('chart.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000,debug=True)
