from django.shortcuts import render, HttpResponse
import datetime
# Create your views here.

class Person(object):
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex
    def say(self):
        return 'my name is' + self.name

def show(request):
    if request.method == 'GET':
        a = request.GET.get('id', 2)
        person = Person('谭咏飞', '20', '男')
        data = {
            'name': '谭振华',
            'age': '22',
            'sex': '男',
            'eng': 'abcdefg',
            'now_time': datetime.datetime.today(),
            'tan': person,
            'id': a
        }

        return render(request, 'show.html', data)





