from django.shortcuts import render

# Create your views here.
def sum(request):
    if request.method=='POST':
        a=int(request.POST.get('txt_num1'))
        b=int(request.POST.get('txt_num2'))
        c=a+b
        return render(request,'Basics/Sum.html',{'Result':c})
    return render(request,'Basics/Sum.html')
    
def calculator(request):
    if request.method=='POST':
        a=int(request.POST.get('txt_num1'))
        b=int(request.POST.get('txt_num2'))
        btn=request.POST.get('btn_submit')
        if btn =='+':
            c=a+b
        elif btn =='-':
            c=a-b
        elif btn =='*':
            c=a*b
        elif btn =='/':
            c=a/b
        return render(request,'Basics/Calculator.html',{'Result':c})
    else:
        return render(request,'Basics/Calculator.html')
