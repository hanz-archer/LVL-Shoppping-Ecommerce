import datetime
from django.shortcuts import render, redirect
from core.models import CartOrder, Product, Category
from django.db.models import Sum
from userauths.models import User
from useradmin.forms import AddProductForm
from django.utils import timezone
from django.db.models import Q

def dashboard(request):
    revenue = CartOrder.objects.aggregate(price=Sum("price"))
    total_orders_count = CartOrder.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by("-id")[:6]
    latest_orders = CartOrder.objects.all()

    this_month = datetime.datetime.now().month
    monthly_revenue = CartOrder.objects.filter(order_date__month=this_month).aggregate(price=Sum("price"))

    
    context = {
        "monthly_revenue": monthly_revenue,
        "revenue": revenue,
        "all_products": all_products,
        "all_categories": all_categories,
        "new_customers": new_customers,
        "latest_orders": latest_orders,
        "total_orders_count": total_orders_count,
    }
    return render(request, "useradmin/dashboard.html", context)



def dashboard_products(request):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    
    context = {
        "all_products": all_products,
        "all_categories": all_categories,
    }
    return render(request, "useradmin/dashboard-products.html", context)


def dashboard_add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            return redirect("useradmin:dashboard-products")
    else:
        form = AddProductForm()
    context = {
        'form':form
    }
    return render(request, "useradmin/dashboard-add-products.html", context)



def dashboard_edit_product(request, pid):
    product = Product.objects.get(pid=pid)

    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.save()
            form.save_m2m()
            return redirect("useradmin:dashboard-products")
    else:
        form = AddProductForm(instance=product)
    context = {
        'form':form,
        'product':product,
    }
    return render(request, "useradmin/dashboard-edit-products.html", context)



def dashboard_delete_product(request, pid):
    product = Product.objects.get(pid=pid)
    product.delete()
    return redirect("useradmin:dashboard-products")

import datetime
from django.shortcuts import render, redirect
from core.models import CartOrder, Product, Category
from django.db.models import Sum
from userauths.models import User
from useradmin.forms import AddProductForm
from django.utils import timezone

# Modify your dashboard view
def dashboard(request):
    # Get the selected date range and specific date from the request's GET parameters
    selected_date = request.GET.get('transactionDate')
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')
    specific_date_str = request.GET.get('specificDate')

    specific_date = datetime.datetime.strptime(specific_date_str, "%Y-%m-%d").date() if specific_date_str else None

    # Fetch orders based on the selected date or all orders if no date is selected
    if selected_date:
        selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        latest_orders = CartOrder.objects.filter(order_date__date=selected_date)
    else:
        latest_orders = CartOrder.objects.all()
    
    if specific_date:
        # Fetch orders for a specific date
        latest_orders = CartOrder.objects.filter(order_date__date=specific_date)
    elif start_date and end_date:
        # Fetch orders within a date range
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        latest_orders = CartOrder.objects.filter(order_date__date__range=[start_date, end_date])
    elif selected_date:
        # Fetch orders based on the selected date
        selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        latest_orders = CartOrder.objects.filter(order_date__date=selected_date)

    # Your existing code for other dashboard data
    revenue = CartOrder.objects.aggregate(price=Sum("price"))
    total_orders_count = CartOrder.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by("-id")[:6]
    this_month = datetime.datetime.now().month
    monthly_revenue = CartOrder.objects.filter(order_date__month=this_month).aggregate(price=Sum("price"))

    context = {
        "monthly_revenue": monthly_revenue,
        "revenue": revenue,
        "all_products": all_products,
        "all_categories": all_categories,
        "new_customers": new_customers,
        "latest_orders": latest_orders,
        "total_orders_count": total_orders_count,
        "selected_date": selected_date,
        "specific_date": specific_date,  # Include the specific date in the context
        "start_date": start_date,  # Include the start date in the context
        "end_date": end_date,  # Include the end date in the context
    }

    return render(request, "useradmin/dashboard.html", context)




