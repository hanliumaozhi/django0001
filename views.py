#coding=utf8

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import MySQLdb

@csrf_exempt
def index(request):
    return render_to_response('han.html', {})


@csrf_exempt
def getImage(request):
    if request.method == 'GET':
        beginNum = request.GET["offset"]
        stepNum = request.GET["count"]
        if beginNum == 17:
            print "test"
        db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', port=3306, db='img', charset='utf8')
        cursor = db.cursor()
        sql = "select * from imgLib where id > %s and id < %s"
        cursor.execute(sql, ((int(beginNum) - 1), (beginNum + stepNum)))
        dataList = list()
        for row in cursor.fetchall():
            temDict = dict()
            temDict["id"] = row[1]
            temDict["liked_count"] = row[2]
            temDict["orig_width"] = row[3]
            temDict["orig_height"] = row[4]
            dataList.append(temDict)
        cursor.close()
        db.commit()
        db.close()

        message = json.dumps(dataList, indent=4)
        return HttpResponse(message, mimetype="application/json")


@csrf_exempt
def likeCount(request):
    if request.method == 'POST':
        db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', port=3306, db='img', charset='utf8')
        cursor = db.cursor()
        sql = "select likeCount from imgLib where id = %s"
        cursor.execute(sql, request.path.split("/")[2])
        count = int(cursor.fetchall()[0][0]) + 1
        sql = " update imgLib set likeCount = %s where id = %s"
        cursor.execute(sql, (count,request.path.split("/")[2]))
        cursor.close()
        db.commit()
        db.close()
        return HttpResponse(count)


class tagData:
    def __init__(self, url, title, count):
        self.url = url
        self.title = title
        self.count = count


@csrf_exempt
def tagging(request):
    if request.method == 'GET':
        db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', port=3306, db='tieba', charset='utf8')
        cursor = db.cursor()
        sql = "select url,title from simpleData where isCheck = 0 limit 20"
        cursor.execute(sql)
        dataList = list()
        num = 0
        for row in cursor.fetchall():
            dataList.append(tagData(row[0], row[1], num))
            num += 1
        cursor.close()
        db.commit()
        db.close()
        c = {'rows': dataList}
        return render_to_response('tagging.html', c)
    elif request.method == "POST":
        print request.POST["ansOfTag"]
        print request.POST["orderOfUrl"]
        tag = request.POST["ansOfTag"].split("##")
        url = request.POST["orderOfUrl"].split("##")
        print len(tag)
        db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', port=3306, db='tieba', charset='utf8')
        cursor = db.cursor()
        sql = "update simpleData set isCheck = 1,isTrue = %s  where url = %s"

        for i in xrange(len(tag)):
            cursor.execute(sql, (tag[i], url[i]))

        print tag[0]
        print url[0]
        cursor.close()
        db.commit()
        db.close()

        message = json.dumps({"true": "true"}, indent=4)
        return HttpResponse(message, mimetype="application/json")
