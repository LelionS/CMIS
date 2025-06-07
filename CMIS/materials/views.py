from django.shortcuts import render, redirect
from .models import Material
from datetime import datetime
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'materials/index.html')
from decimal import Decimal
from datetime import datetime
from decimal import Decimal
from datetime import datetime
from .models import MaterialCategory  # Make sure this is imported
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def add_material(request):
    if request.method == 'POST':
        category_id = request.POST['category']
        category = MaterialCategory.objects.get(id=category_id)
        name = request.POST['name']
        quantity = int(request.POST['quantity'])
        unit = request.POST['unit']
        supplier = request.POST['supplier']
        unit_cost = Decimal(request.POST['unit_cost'])
        delivery_date = datetime.strptime(request.POST['delivery_date'], '%Y-%m-%d').date()
        amount_in_stock = int(request.POST['amount_in_stock'])
        image = request.FILES.get('image')

        material = Material(
            category=category,
            name=name,
            quantity=quantity,
            unit=unit,
            supplier=supplier,
            unit_cost=unit_cost,
            delivery_date=delivery_date,
            amount_in_stock=amount_in_stock,
            image=image,
        )
        material.save()
        return redirect('add-material')

    categories = MaterialCategory.objects.all()  # Query categories
    return render(request, 'materials/add_material.html', {'categories': categories})




from .models import Material
@login_required
def material_list(request):
    materials = Material.objects.all()
    return render(request, 'materials/material_list.html', {'materials': materials})

from django.shortcuts import render, redirect, get_object_or_404
from .models import MaterialRequest, Material
from datetime import date
from django.contrib.auth.decorators import login_required

@login_required
def request_material(request):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        material_id = int(request.POST['material_id'])
        material = Material.objects.get(id=material_id)

        # Use logged-in user as requester
        requester = request.user

        new_request = MaterialRequest(
            material=material,
            quantity_requested=quantity,
            requested_by=requester,
            status='Pending'
        )
        new_request.save()

        return redirect('view_my_requests')

    materials = Material.objects.filter(amount_in_stock__gt=0)
    return render(request, 'materials/request_material.html', {'materials': materials})


@login_required
def view_requests(request):
    requests = MaterialRequest.objects.all().order_by('-request_date')
    return render(request, 'materials/view_requests.html', {'requests': requests})

from django.utils import timezone

@login_required
def approve_request(request, request_id):
    material_request = get_object_or_404(MaterialRequest, id=request_id)

    if material_request.status == 'Pending' and material_request.quantity_requested <= material_request.material.amount_in_stock:
        material_request.status = 'Approved'
        material_request.status_updated_by = request.user
        material_request.status_updated_at = timezone.now()

        material_request.material.amount_in_stock -= material_request.quantity_requested
        material_request.material.save()
        material_request.save()
    
    return redirect('view_requests')

@login_required
def decline_request(request, request_id):
    material_request = get_object_or_404(MaterialRequest, id=request_id)

    if material_request.status == 'Pending':
        material_request.status = 'Declined'
        material_request.status_updated_by = request.user
        material_request.status_updated_at = timezone.now()
        material_request.save()

    return redirect('view_requests')

@login_required
def shop_home(request):
    items = Material.objects.filter(is_available=True)
    return render(request, 'materials/shop_home.html', {'items': items})

@login_required
def view_my_requests(request):
    requests = MaterialRequest.objects.filter(requested_by=request.user).order_by('-request_date')
    return render(request, 'materials/my_requests.html', {'requests': requests})