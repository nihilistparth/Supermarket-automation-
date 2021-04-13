from django.shortcuts import render,redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm,EditProductForm,TransactionForm
from .models import Product,Transaction
from django.views import generic
from django.contrib.auth.models import User
from .checks import *
from django.http import HttpResponse
from .utils import render_to_pdf
import datetime
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response




@user_passes_test(lambda u: u.is_superuser)
def home(request):
    return render(request,'product/home.html')

@user_passes_test(lambda u: u.is_superuser)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        # {'name':"rice", 'price':150}
        if form.is_valid():
            form.save()
            messages.success(request, f'Product added!')
            return redirect('product-home')

    else:
        form = ProductForm()
    return render(request,'product/add_product.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def edit_product(request):

    context = {'product_list': Product.objects.all()}
    return render(request,'product/edit_product.html',context)


@user_passes_test(lambda u: u.is_superuser)
def edit_util(request,p_id):
    if request.method == 'POST':
        form = EditProductForm(request.POST)
        product = Product.objects.get(pk = p_id)
        if form.is_valid():
            product.quantity = form.cleaned_data['quantity']
            product.selling_price = form.cleaned_data['selling_price']
            product.cost_price = form.cleaned_data['cost_price']
            
            if product.selling_price<product.cost_price:
                context = {'form':form,'product':product,'my_error_message':"Selling Price cannot be less than Cost Price!"}
                return render(request,'product/edit_util.html',context)

            product.save()
            messages.success(request, f'{product.name} has been edited!')
            return redirect('product-edit')
            
        else:
            context = {'form':form,'product':product}
            return render(request,'product/edit_util.html',context)


    product = Product.objects.get(pk=p_id)
    form = EditProductForm(initial={'cost_price':product.cost_price,'quantity':product.quantity,'selling_price':product.selling_price})
    context = {'form':form,'product':product}
    return render(request,'product/edit_util.html',context)

@login_required
def view_product(request):
    form = ProductForm()
    context = {'product_list':Product.objects.all(),'form':form}
    return render(request, 'product/view_product.html', context)

@login_required
def new_transaction(request):

    if request.method == 'POST':
    
        form = TransactionForm(request.POST)

        if form.is_valid():
            
            p_name = form.cleaned_data['Product_name']
            p_id = form.cleaned_data['product_id']

            if p_id==None and len(p_name)==0 :
                product_list = []
                for key in request.session['my_dict'].keys():
                    p = Product.objects.get(name=key)
                    product_list.append(p)
                context = {'form':form,'product_dict':request.session['my_dict'],'product_list':product_list,'my_error_message':f'Enter a valid ID and / or Product Name'}
                return render(request,'product/transaction.html',context)
            
            if p_id!=None and len(p_name) == 0 :
                temp = Product.objects.filter(pk=p_id)

                if  len(temp)==0 :
                    product_list = []
                    for key in request.session['my_dict'].keys():
                        p = Product.objects.get(name=key)
                        product_list.append(p)

                    context = {'form':form,'product_dict':request.session['my_dict'],'product_list':product_list,'my_error_message':f'Please enter a valid ID!'}
                    return render(request,'product/transaction.html',context)
                
                p_name = Product.objects.get(pk=p_id).name 
            
            elif p_id==None and len(p_name)!=0 :
                pass
            
            elif p_id!=None and len(p_name)!=0 :
                temp = Product.objects.filter(pk=p_id)
                if  len(temp)==0 :
                    product_list = []
                    for key in request.session['my_dict'].keys():
                        p = Product.objects.get(name=key)
                        product_list.append(p)
                    context = {'form':form,'product_dict':request.session['my_dict'],'product_list':product_list,'my_error_message':f'Please enter a valid ID!'}
                    return render(request,'product/transaction.html',context)

                if p_name != Product.objects.get(pk=p_id).name :
                    product_list = []
                    for key in request.session['my_dict'].keys():
                        p = Product.objects.get(name=key)
                        product_list.append(p)

                    context = {'form':form,'product_dict':request.session['my_dict'],'product_list':product_list,'my_error_message':f'Name: {p_name} and ID: {p_id} are mismatched!'}
                    return render(request,'product/transaction.html',context)
                  

            # product_exist check...
            if not product_exist(p_name):
                product_list = []
                for key in request.session['my_dict'].keys():
                    p = Product.objects.get(name=key)
                    product_list.append(p)

                context = {'form':form,'product_dict':request.session['my_dict'],'product_list':product_list,'my_error_message':f'{p_name} is not available!'}
                return render(request,'product/transaction.html',context)

            p = Product.objects.filter(name__exact = p_name)[0]
            
            if 'my_dict' not in request.session:
                request.session['my_dict'] = {}

            
            # check if current product is not in 'my_dict'
            if p_name not in request.session['my_dict'].keys():

                if form.cleaned_data['quantity'] > p.quantity:
                
                    product_list = []
                    for key in request.session['my_dict'].keys():
                        temp = Product.objects.get(name=key)
                        product_list.append(temp)

                    context = {'form':form,'product_dict':request.session['my_dict'],'product_list':product_list,'my_error_message':f'Only {p.quantity} item(s) left in stock'}
                    return render(request,'product/transaction.html',context)
                
                else:
                    request.session['my_dict'][p_name] = 0 
                
                
                
            # checks if entered quantity exceeds the stock limit...
            if quantity_check(p.id, form.cleaned_data['quantity'] + request.session['my_dict'][p_name]):            

                if 'my_dict' not in request.session:
                    request.session['my_dict'] = {}

                if p_name in request.session['my_dict'].keys():
                    request.session['my_dict'][p_name] += form.cleaned_data['quantity'] 
                    
                else:
                    request.session['my_dict'][p_name] = form.cleaned_data['quantity']

                return redirect('product-transaction')
                
            else:

                if 'my_dict' not in request.session:
                    request.session['my_dict'] = {}
                
                product_list = []
                for key in request.session['my_dict'].keys():
                    p = Product.objects.get(name=key)
                    product_list.append(p)

                context = {'form':form,'product_dict':request.session['my_dict'],'product_list':product_list,'my_error_message':f'Only {p.quantity} item(s) left in stock'}
                return render(request,'product/transaction.html',context)
    
    form = TransactionForm()
    # t = Transaction.objects.filter(user=request.user).order_by('-created_at')[0]
    if 'my_dict' not in request.session:
        request.session['my_dict'] = {}

    product_list = []
    for key in request.session['my_dict'].keys():
        p = Product.objects.get(name=key)
        product_list.append(p)

    context = {'form':form, 'product_dict':request.session['my_dict'], 'product_list':product_list}
    return render(request, 'product/transaction.html', context)

# def generate_pdf(request):
# Before rendering out the pdf, make sure to decrease the size of the inventory...

def generate_pdf(request):

    transaction_dict = request.session['my_dict']
    sp = {}
    cp = {}

    total_amount = 0

    product_list = []

    for key,val in transaction_dict.items():
        p = Product.objects.get(name__exact=key)
        p.quantity -= val
        p.save()
        total_amount += p.selling_price*val
        product_list.append(p)
        sp[key] = p.selling_price
        cp[key] = p.cost_price

    t = Transaction.objects.create(user=request.user, data=transaction_dict ,amount = total_amount, sp=sp, cp=cp)
    
    del request.session['my_dict']


    data = {
             'product_list': product_list,
             'amount': total_amount,
             'today': datetime.date.today(), 
             'product_dict': transaction_dict,
             'order_id': t.id,
        }
    pdf = render_to_pdf('product/invoice.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def complete_transaction(request):
    return render(request, 'product/complete_transaction.html')


def clear(request):
    del request.session['my_dict']
    return redirect('product-transaction')

@user_passes_test(lambda u: u.is_superuser)
def user_report(request, u_id):
    user = User.objects.get(pk=u_id)
    transactions = user.transaction_set.all().order_by('-created_at')
    context = {'transactions':transactions, 'username':user.username, 'u_id':user.id}
    return render(request,'product/user_transaction.html', context)

@user_passes_test(lambda u: u.is_superuser)
def report(request):

    num = Transaction.objects.all().count()
    user_list = User.objects.all()

    if request.method == "POST":
        start = request.POST['start_date']
        end = request.POST['end_date']

        if date_correct(start, end) == 1:
            start_obj = datetime.date(int(start[0:4]),int(start[5:7]),int(start[8:]))
            end_obj = datetime.date(int(end[0:4]),int(end[5:7]),int(end[8:])+1)

            if (start_obj >= end_obj):
                context = {
                    'num':num,
                    'user_list': user_list,
                    'my_error_message': 'Start Date cannot occur before the End Date'}
                return render(request,'product/report.html',context)

        elif date_correct(start, end) == 2:
            end_obj = datetime.date.today()
            year = end_obj.strftime("%Y")
            month = end_obj.strftime("%m")
            day = end_obj.strftime("%d")
            end = year+'-'+month+'-'+day

        else:
            context = {
                'num':num,
                'user_list': user_list,
                'my_error_message': 'Please enter the appropriate Start Date'}
            return render(request,'product/report.html',context)

        request.session['start'] = start
        request.session['end'] = end        
        
        return redirect('product-chart-home')

    context = {
        'num':num,
        'user_list': user_list,
    }
    return render(request,'product/report.html',context)

@user_passes_test(lambda u: u.is_superuser)
def chart_home(request):
    return render(request, 'product/chart.html')


@user_passes_test(lambda u: u.is_superuser)
def create_chart(request):
    start = request.session['start']
    end = request.session['end']

    del request.session['start']
    del request.session['end']

    start_obj = datetime.date(int(start[0:4]),int(start[5:7]),int(start[8:]))
    end_obj = datetime.date(int(end[0:4]),int(end[5:7]),int(end[8:])+1)

    object_list = []
    quantity_list = []
    profit_list = []
    revenue_list = []

    transaction_list = Transaction.objects.all().filter(created_at__gte=start_obj).filter(created_at__lte=end_obj)

    for transaction in transaction_list:
        for key,val in transaction.data.items():
            if key not in object_list:
                object_list.append(key)
                quantity_list.append(val)
                profit_list.append((transaction.sp[key]-transaction.cp[key])*val)
                revenue_list.append(transaction.sp[key]*val)
            
            else:
                ind = object_list.index(key)
                quantity_list[ind]+=val
                profit_list[ind] += (transaction.sp[key]-transaction.cp[key])*val
                revenue_list[ind] += transaction.sp[key]*val
                
    data = {
        'object_list':object_list,
        'quantity_list':quantity_list,
        'profit_list':profit_list,
        'revenue_list':revenue_list,
    }

    return JsonResponse(data)