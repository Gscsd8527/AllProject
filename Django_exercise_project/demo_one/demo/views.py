from django.shortcuts import render
from django.db import connection
# Create your views here.

def ShowData(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        sql = "select * from gushi"
        cursor.execute(sql)
        data = cursor.fetchall()[:10]
        return render(request, 'show.html', {'order': data})
