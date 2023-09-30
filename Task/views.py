from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from Task.models import taskModel
# Create your views here.

def signUpIn(request):
    if 'name' in request.session:
        user1 = request.session['name']
        request.session.set_expiry(3600)
        allData = taskModel.objects.all()
        pendingLen = len(taskModel.objects.filter(status='Pending'))
        inprogLen = len(taskModel.objects.filter(status='In-progress'))
        compLen = len(taskModel.objects.filter(status='Completed'))
        data = {
            'user':user1,
            'allData':allData,
            'pendingLen':pendingLen,
            'inprogLen':inprogLen,
            'compLen':compLen,
        }
        print('>>>>>>>>',request.session['name'])
        return render(request,'view_task.html' ,data)
    
    else:
        if request.method=='POST':
            if request.POST.get('form_type') == 'signup1':
                fname = request.POST.get('first_name')
                lname = request.POST.get('last_name')
                email = request.POST.get('email')
                user1 = request.POST.get('username')
                passwd = request.POST.get('passwd1')
                passwd2 = request.POST.get('passwd2')
                if passwd==passwd2:
                    data = User.objects.create_user(first_name=fname,last_name=lname,email=email,username=user1,password=passwd)
                    data.save()
                    print(fname,lname,email,user1,passwd,sep='\n')
                else:
                    return render(request,'login.html',{'fn':True})
            
            elif request.POST.get('form_type') == 'login1':
                user1 = request.POST.get('username')
                passwd = request.POST.get('passwd') 
                user = auth.authenticate(username=user1,password=passwd)
                if user is not None:
                    auth.login(request,user)
                    request.session['name'] = user1
                    request.session.set_expiry(3600)
                    allData = taskModel.objects.all()
                    pendingLen = len(taskModel.objects.filter(status='Pending'))
                    inprogLen = len(taskModel.objects.filter(status='In-progress'))
                    compLen = len(taskModel.objects.filter(status='Completed'))
                    data = {
                        'user':user1,
                        'allData':allData,
                        'pendingLen':pendingLen,
                        'inprogLen':inprogLen,
                        'compLen':compLen,
                    }
                    
                    return render(request,'view_task.html',data)
    return render(request,'login.html')


def logout(request):
    del request.session['name']
    return redirect('/')

def addTask(request):
    if 'name' in request.session:
        user1 = request.session['name']
        if request.method=='POST':
            
            comp_Name = request.POST.get('company')
            task_Name = request.POST.get('task')
            task_desc = request.POST.get('description')
            status = request.POST.get('work_status')
            task_Create = request.POST.get('allocation_date')
            sDate = request.POST.get('start_date')
            sTime = request.POST.get('start_time')
            eDate = request.POST.get('end_date')
            eTime = request.POST.get('end_time')
            mydb = taskModel(assign_to='',created_by=user1,comp_Name=comp_Name,task_Name=task_Name,task_Desc=task_desc,status=status,task_Create=task_Create,start_Date=sDate,start_Time=sTime,end_Date=eDate,end_Time=eTime)
            mydb.save()
            print(request.user.first_name,'<<<<')
            print(comp_Name,task_Name,status,task_Create,sep='\n')
        # request.session.set_expiry(30)
        print('>>>>>>>>',request.session['name'])
        return render(request,'add_task.html' ,{'user':user1})

def viewTask(request):
    if 'name' in request.session:
        user1 = request.session['name']
        allData = taskModel.objects.all()
        pendingLen = len(taskModel.objects.filter(status='Pending'))
        inprogLen = len(taskModel.objects.filter(status='In-progress'))
        compLen = len(taskModel.objects.filter(status='Completed'))
        data = {
            'user':user1,
            'allData':allData,
            'pendingLen':pendingLen,
            'inprogLen':inprogLen,
            'compLen':compLen,
        }
        print(data)
        print(pendingLen)
        for i in allData:
            print(i.comp_Name)
        # request.session.set_expiry(30)
        print('>>>>>>>>',request.session['name'])
        return render(request,'view_task.html',data)
    
def assignTask(request):
    if 'name' in request.session:
        user1 = request.session['name']
        print('>>>>>>>>',request.session['name'])
        all_users = list(User.objects.values('username'))
        pendingLen = len(taskModel.objects.filter(status='Pending'))
        inprogLen = len(taskModel.objects.filter(status='In-progress'))
        compLen = len(taskModel.objects.filter(status='Completed'))
        assignData = taskModel.objects.filter(assign_by=user1)
        if request.method=='POST':
            assignTo = request.POST.get('employee_name')
            assignBy = user1
            comp_Name = request.POST.get('company')
            task_Name = request.POST.get('task')
            task_desc = request.POST.get('description')
            status = request.POST.get('work_status')
            task_Create = request.POST.get('allocation_date')
            sDate = request.POST.get('start_date')
            sTime = request.POST.get('start_time')
            eDate = request.POST.get('end_date')
            eTime = request.POST.get('end_time')
            dDate = request.POST.get('deadline')
            mydb = taskModel(assign_to=assignTo,assign_by=assignBy,created_by=user1,comp_Name=comp_Name,task_Name=task_Name,task_Desc=task_desc,status=status,task_Create=task_Create,start_Date=sDate,start_Time=sTime,end_Date=eDate,end_Time=eTime,deadline_Date=dDate)
            mydb.save()
        allData = {
            'user':user1,
            'assignData':assignData,
            'all_users':all_users,
            'pendingLen':pendingLen,
            'inprogLen':inprogLen,
            'compLen':compLen
        }
        return render(request,'assign_task.html' ,allData)

def updateTask(request,sid):
    if 'name' in request.session:
        user1 = request.session['name']
        upData = taskModel.objects.get(id=sid)
        fname = request.user.first_name
        return render(request,'edit_form.html' ,{'user':user1,'upData':upData,'fname':fname})
    

def updateTaskTo(request,sid):
    if 'name' in request.session:
        user1 = request.session['name']
        print('>>> Views Task To')
        fname = request.user.first_name
        upData = taskModel.objects.get(id=sid)
        if request.method=='POST':
            upData.comp_Name = request.POST.get('company')
            upData.task_Name = request.POST.get('task')
            upData.task_Desc = request.POST.get('description')
            upData.status = request.POST.get('work_status')
            upData.task_Create = request.POST.get('allocation_date')
            upData.start_Date = request.POST.get('start_date')
            upData.start_Time = request.POST.get('start_time')
            upData.end_Date = request.POST.get('end_date')
            upData.end_Time = request.POST.get('end_time')
            upData.save()
            print(request.user.first_name,'<<<<')
        return redirect('/viewtask')


def pendingTask(request):
    if 'name' in request.session:
        pending = taskModel.objects.filter(status='Pending')
        pendingLen = len(taskModel.objects.filter(status='Pending'))
        inprogLen = len(taskModel.objects.filter(status='In-progress'))
        compLen = len(taskModel.objects.filter(status='Completed'))
        for i in pending:
            print(i.task_Name)
        allData = {
            'pending':pending,
            'pendingLen':pendingLen,
            'inprogLen':inprogLen,
            'compLen':compLen
        }
        return render(request,'pending_task.html',allData)

def inprogressTask(request):
    if 'name' in request.session:
        inprog = taskModel.objects.filter(status='In-progress')
        pendingLen = len(taskModel.objects.filter(status='Pending'))
        inprogLen = len(taskModel.objects.filter(status='In-progress'))
        compLen = len(taskModel.objects.filter(status='Completed'))
        for i in inprog:
            print(i.task_Name)
        allData = {
            'inprog':inprog,
            'pendingLen':pendingLen,
            'inprogLen':inprogLen,
            'compLen':compLen
        }
        return render(request,'inprogress_task.html',allData)

def completedTask(request):
    if 'name' in request.session:
        completed = taskModel.objects.filter(status='Completed')
        pendingLen = len(taskModel.objects.filter(status='Pending'))
        inprogLen = len(taskModel.objects.filter(status='In-progress'))
        compLen = len(taskModel.objects.filter(status='Completed'))
        for i in completed:
            print(i.task_Name)
        allData = {
            'completed':completed,
            'pendingLen':pendingLen,
            'inprogLen':inprogLen,
            'compLen':compLen
        }
        return render(request,'completed_task.html',allData)

def deleteAssignTask(request,sid):
    if 'name' in request.session:
        dataDel = taskModel.objects.get(id=sid)
        dataDel.delete()
        return redirect('/viewtask')

