from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from cryptography.fernet import Fernet

import pytz
import random
import math
import requests

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect

from ..models import *
from .. import models
from ..views import all_active_candidates, active_status

BLANK = ''
POST_METHOD = "POST"
OTP_HTML = 'csp_app/otp.html'
DASHBOARD_VIEW = 'csp_view:dashboard'
LOGGED_IN_SUCCESSFULLY = 'Logged in Successfully'
OTP_SENT = "OTP Sent To Registered Mobile Number"
INVALID_CREDENTIALS = "Invalid Credentials"


@login_required(login_url='/notlogin/')
def admin(request):
    return render(request, 'csp_app/adminhome.html', {'allcandidates': all_active_candidates, })


def csp_login(request):
    if request.method == "POST":
        if request.POST.get('username') != None or request.POST.get('username') != '':
            usrname = request.POST.get('username')
            pwd = request.POST.get('password')
            if usrname == '':
                messages.add_message(request, messages.WARNING, "Please Enter UID")
                return redirect('csp_app:login')
            if pwd == '':
                messages.add_message(request, messages.WARNING, "Please Enter Password")
                return redirect('csp_app:login')

            if request.POST.get('otp') != None:
                user = 'check for otp'

            user = authenticate(request, username=usrname, password=pwd)
            if user is not None and user.is_active:
                # x = otp = send_me_otp()
                x = otp = send_otp(request)
                print(otp)
                key = Fernet.generate_key()
                f = Fernet(key)
                otp_value = bytes(otp, 'utf-8')
                encrpt_otp = f.encrypt(otp_value)

                OTP = str(encrpt_otp, 'utf-8')

                key = str(key, 'utf-8')
                messages.success(request, OTP_SENT)
                return render(request, OTP_HTML, {'otp': OTP, 'f': key, 'uid': usrname, 'pwd': pwd, 'x': x})

            else:
                messages.add_message(request, messages.ERROR, INVALID_CREDENTIALS)
                return render(request, 'csp_app:login')

        else:
            messages.add_message(request, messages.ERROR, "Invalid Credentials")
            return redirect('csp_app:login')
    return render(request, 'csp_app/Login.html', {'allcandidates': all_active_candidates, })


@login_required(login_url='/notlogin/')
def csp_logout(request):
    logout(request)
    return redirect('csp_app:login')


def notlogin(request):
    return render(request, 'csp_app/timeout.html', {'allcandidates': all_active_candidates, })


def check_otp(request):
    if request.method == 'POST':
        if request.POST.get('otp') != BLANK:
            uid = request.POST.get('uid')
            pwd = request.POST.get('pwd')
            sent_otp = request.POST.get('sent_otp')
            key = request.POST.get('general')
            key = bytes(key, 'utf-8')
            f = Fernet(key)
            OTP = bytes(sent_otp, 'utf-8')
            otp = f.decrypt(OTP)
            otp = str(otp, 'utf-8')
            inserted_otp = request.POST.get('otp')
            user = authenticate(request, username=uid, password=pwd)

            if inserted_otp == otp:
                login(request, user)
                try:
                    User.objects.filter(pk=request.user.pk).update(last_login=datetime.datetime.now())
                    group = request.user.groups.all()

                    for groupname in group:
                        group_name = groupname
                    if str(group_name) == 'Admin':
                        messages.success(request, "Login Successfull")
                        return redirect('csp_app:candidate')
                    elif str(group_name) == 'Vendor':
                        messages.success(request, "Login Successfull")
                        return redirect('csp_app:candidate')
                    elif str(group_name) == 'Candidate':
                        try:
                            selected_candidate = master_candidate.objects.get(Personal_Email_Id=str(request.user),
                                                                              status=active_status)
                        except ObjectDoesNotExist:
                            messages.add_message(request, messages.ERROR, "Invalid Credentials")
                            return redirect('csp_app:login')
                        messages.success(request, "Login Successfull")
                        return redirect('csp_app:document_upload', selected_candidate.pk_candidate_code)
                    else:
                        messages.success(request, "Login Successfull")
                        return redirect('csp_app:candidate')
                except UnboundLocalError:
                    messages.success(request, "Login Successfull")
                    return redirect('csp_app:rm_joined')

            else:
                messages.add_message(request, messages.ERROR, 'Incorrect OTP Try Again')
                x = 'Use Previous OTP'
                return render(request, OTP_HTML, {'otp': request.POST.get('sent_otp'), 'f': request.POST.get('general'),
                                                  'uid': request.POST.get('uid'), 'pwd': request.POST.get('pwd'),
                                                  'x': x})

    return render(request, OTP_HTML)


def send_otp(request):
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])

    url = 'https://alerts.kaleyra.com/api/v4/?api_key=Af25bf56645bb5c944ed22af307bd97b7'
    message = '# DO NOT SHARE: ' + random_str + ' is the otp for your on boarding tool login account. Keep this OTP to yourself for account safety.'

    # phone_number = '8802999088'
    # phone_number = '9711772297'
    # phone_number = '8197736577'
    # phone_number = '9663473089'
    # phone_number = '9008453786'
    # phone_number = '9582420365'
    print('sdf')
    print(request.POST['username'])
    if request.POST['username'] != None:
        emp_record = User.objects.get(**{'username': request.POST['username'], 'is_active': True})
    else:
        emp_record = User.objects.get(**{'username': request.POST['uid'], 'is_active': True})
    phone_record = user_phone.objects.get(**{'user': emp_record})
    phone_number = getattr(phone_record, 'phone')
    print(phone_number)

    sender_id = 'HLPUDN'
    base_url = url + '&method=sms&message=' + message + '&to=' + phone_number + '&sender=' + sender_id + "&template_id=1"

    x = requests.post(base_url)
    print(x.text)
    return random_str


def send_me_otp():
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    url = 'https://alerts.kaleyra.com/api/v4/?api_key=Af25bf56645bb5c944ed22af307bd97b7'
    message = '# DO NOT SHARE: ' + random_str + ' is the otp for your hrms login account. Keep this OTP to yourself for account safety.'
    phone_number = '9663473089'
    sender_id = 'HLPUDN'
    base_url = url + '&method=sms&message=' + message + '&to=' + phone_number + '&sender=' + sender_id + "&template_id=1"
    return random_str


def resend_otp(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        pwd = request.POST.get('pwd')
        # x = otp = send_me_otp()
        x = otp = send_otp(request)
        print("after x")
        key = Fernet.generate_key()
        f = Fernet(key)
        otp_value = bytes(otp, 'utf-8')
        encrpt_otp = f.encrypt(otp_value)

        OTP = str(encrpt_otp, 'utf-8')

        key = str(key, 'utf-8')
        return render(request, OTP_HTML, {'otp': OTP, 'f': key, 'uid': uid, 'pwd': pwd, 'x': x})
    return render(request, OTP_HTML)
