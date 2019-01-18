from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View
from django.http import JsonResponse



class CalendarView(View):
    """日历"""
    def get(self,requset):

        return render(requset,'xadmin/calendar.html')


