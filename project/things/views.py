from django.shortcuts import *
from .forms import StudentLoginForm,PhotoForm
from .models import Student,TestInfo,CheatingReport,Question,Option,TestResult,Answer,SelectedOption
from .mixin import TestLinkMixin
import face_recognition
import cv2
import json
import numpy as np
import os
import random
import datetime 
from django.views.generic import View,TemplateView
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.core.exceptions import ValidationError
from least.settings import BASE_DIR

path = BASE_DIR
image_path = path + "/media/students/"
# Create your views here.
# для того что бы сравнить фото с видео 
def facedect(loc):
        cam = cv2.VideoCapture(0)   #включить камеру
        s, img = cam.read()
        if s: #проверка камеры
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                
                MEDIA_ROOT =os.path.join(BASE_DIR) #путь до фотки
                
                loc=(str(MEDIA_ROOT)+loc)
                face_1_image = face_recognition.load_image_file(loc)
                print(face_1_image)
                print(face_recognition.face_encodings(face_1_image))
                face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0] #перевести фотку в массив

                face_locations = face_recognition.face_locations(img) #из видео получить лицо
                if face_locations: #если есть лицо
                    face_encodings = face_recognition.face_encodings(img, face_locations) #перевести лицо в массив
                    check=face_recognition.compare_faces(face_1_face_encoding, face_encodings) #проверка на совместимость
                    print(check)
                    if check[0]:
                            return True
                    else :
                            return False   

def create_photo(id):
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(path + '/cascade/haarcascade_frontalface_alt2.xml')
    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        print(faces)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x+5000,y+5000),(x+w+5000,y+h+5000),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            print(image_path + str(id))
            print(os.path.isfile(image_path + str(id)))
            if not os.path.isfile(image_path + str(id)):# надо сделать что то с тем если папка существует
                os.makedirs(image_path + str(id))
            image = image_path + str(id)+ "/image.png"
            image_item ="/students/" + str(id)+"/image.png"
            cv2.imwrite(image,roi_gray)
            return image_item 

class StudentLoginView(TestLinkMixin,View):
    login_url = "notAvailable/404"
    def get(self,request,uidb64):
        form = StudentLoginForm()
        test_id = force_text(urlsafe_base64_decode(uidb64))
        test = TestInfo.objects.get(id=test_id)
        return render(request,'reg1.html',{"form":form,"test":test,"uidb64":uidb64})
    
    def post(self,request,uidb64):
        bound_form = StudentLoginForm(request.POST)
        test_id = force_text(urlsafe_base64_decode(uidb64))
        test = TestInfo.objects.get(id=test_id)
        if bound_form.is_valid() :
            user = Student.objects.get(id = bound_form.cleaned_data['id'])
            if user in test.students.all():
                if user.photo != "":
                    try:
                        if not facedect(user.photo.url):
                            message = "Are you sure you are {}'s user?".format(user.id)
                            return render(request,'reg1.html',{"form":bound_form,"message":message,"uidb64":uidb64})  
                        else:
                            uidb64_student=urlsafe_base64_encode(force_bytes(bound_form.cleaned_data['id']))
                            return redirect('reg3',uidb64,uidb64_student)
                    except:
                        uidb64_student=urlsafe_base64_encode(force_bytes(bound_form.cleaned_data['id']))
                        return redirect('uploadPhoto',uidb64,uidb64_student)
                else:
                    try:
                        user.photo = create_photo(user.id)
                        user.save()
                        uidb64_student=urlsafe_base64_encode(force_bytes(bound_form.cleaned_data['id']))
                        return redirect('reg3',uidb64,uidb64_student)
                    except:
                        uidb64_student=urlsafe_base64_encode(force_bytes(bound_form.cleaned_data['id']))
                        return redirect('uploadPhoto',uidb64,uidb64_student)
            return render(request,'reg1.html',{"form":bound_form,"message":"You are not alloweded to pass test","uidb64":uidb64})  
        return render(request,'reg1.html',{"form":bound_form,"uidb64":uidb64})  


class UploadPhoto(TestLinkMixin,View):
    def get(self,request,uidb64,uidb64_student):
        form = PhotoForm()
        test_id = force_text(urlsafe_base64_decode(uidb64))
        test = TestInfo.objects.get(id=test_id)
        return render(request,'uploadPhoto.html',{"form":form,"uidb64_student":uidb64_student,"uidb64":uidb64})
    def post(self,request,uidb64,uidb64_student):
        form = PhotoForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            student_id = force_text(urlsafe_base64_decode(uidb64_student))
            user = Student.objects.get(id = student_id)
            print(form.cleaned_data['photo'])
            user.photo = form.cleaned_data['photo']
            user.save()
            return redirect('reg3',uidb64,uidb64_student)
        return render(request,'uploadPhoto.html',{"form":bound_form,"uidb64_student":uidb64_student,"uidb64":uidb64})  
 
class NotYet(TemplateView):
    template_name = "not_available.html"



class TestInfoView(TestLinkMixin,TemplateView):
    template_name = "reg3.html"
  

class TestView(TestLinkMixin,TemplateView):
    template_name = "new_student_section.html"
    def get(self,request,uidb64,uidb64_student):
        student_id = force_text(urlsafe_base64_decode(uidb64_student))
        test_id = force_text(urlsafe_base64_decode(uidb64))
        test = get_object_or_404(TestInfo, id=test_id)
        student= get_object_or_404(Student, id=student_id)
        testResult = TestResult.objects.get(test=test,student=student)
        if testResult.started_time is not None:
            return redirect("NotYet")
        end = datetime.datetime.combine(test.start_date,
                                        test.end_time)
        time_left = end - datetime.datetime.now()
        testResult.started_time =  datetime.datetime.now()
        testResult.save()
        minuts =  test.duration if time_left.seconds < 360 else int(time_left.seconds / 60)
        seconds =  0 if time_left.seconds < 360 else time_left.seconds % 60
        duration =  test.duration if time_left.seconds < 360 else int(time_left.seconds)
        return render(request,"new_student_section.html", {'questions': test.questions.all(),"duration":duration,'minuts':minuts,"seconds":seconds,'uidb64_student' :uidb64_student })

def result(request,uidb64_student,uidb64):
    point = 0
    test_id = force_text(urlsafe_base64_decode(uidb64))
    student_id = force_text(urlsafe_base64_decode(uidb64_student))
    test = get_object_or_404(TestInfo, id=test_id)
    student= get_object_or_404(Student, id=student_id)
    testResult = TestResult.objects.get(test=test,student=student)
    totalQuestions =  Question.objects.filter(test = test).count()
    if request.is_ajax() and request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        for data in json_data:
            question = Question.objects.get(id = data['id'])
            correct = Option.objects.filter(question = question,is_correct=True)
            answer = Answer(test = testResult,question=question)
            answer.save()
            if question.is_multiple_choice and len(data['options']) > 1:
                for options in data['options']:
                    option = Option.objects.get(id = options,question = question)
                    record = SelectedOption(answer = answer,option=option)
                    if options in correct:
                        point += 1
                    record.save()
            elif (not question.is_multiple_choice )and len(data['options']) == 1:
                option = Option.objects.get(id = int(data['options'][0]),question = question)
                record = SelectedOption(answer = answer,option=option)
                if str(data['options'][0]) == str(correct[0].id):
                        point += 1
                record.save()
        print(point)
        testResult.grade = (point/totalQuestions)*100
        print(datetime.date.today())
        testResult.submitted_date = datetime.datetime.now()
        #  = TesttestResult(student = student,test=test,grade=point,submitted_date = datetime.date.today )
        print(1234)
        testResult.save()
    return render(request, 'result.html')


def checkStudent(request,uidb64_student,uidb64):
    student_id = force_text(urlsafe_base64_decode(uidb64_student))
    user = Student.objects.get(id = student_id)
    test_id = force_text(urlsafe_base64_decode(uidb64))
    if not facedect(user.photo.url):
        writingReport(student_id,test_id,"Person can't be identifier")
    elif  facedect(user.photo.url):
        return JsonResponse({'response': 'Student was successfully identificated'}, status=200)

    return JsonResponse({'error': 'ajax request is required'}, status=400)

def saveCheatingReport(request,uidb64_student,uidb64):
    student_id = force_text(urlsafe_base64_decode(uidb64_student))
    test_id = force_text(urlsafe_base64_decode(uidb64))
    writingReport(student_id,test_id,json.loads(request.body.decode('utf-8')))
    return JsonResponse({'response': 'Cheating was successfully saved'}, status=200)

def writingReport(student_id,test_id,reason):
    user = Student.objects.get(id = student_id)
    report = CheatingReport()
    report.student = user
    report.test = TestInfo.objects.get(id=test_id)
    report.cheating_date = datetime.date.today
    report.reason = reason
    report.save()