from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .models import Skin, User, OwnedSkin, Sale, SaleItem, Auction
from django.contrib.contenttypes.models import ContentType
from django.db.models import Value, CharField
from itertools import chain

# Create your views here.

def dashboard(request):
    return render(request,'main/dashboard.html')

def skin(request, skin_name):
    skin = get_object_or_404(Skin, name=skin_name)
    try:
        skin_content_type = ContentType.objects.get_for_model(Skin)
        sale_items = SaleItem.objects.filter(content_type=skin_content_type,object_id=skin.id)
        sales = Sale.objects.filter(items__in=sale_items).annotate(type=Value('sale',output_field=CharField()))
        auctions = Auction.objects.filter(item=skin).annotate(type=Value('auction',output_field=CharField()))
        combined = chain(sales,auctions)
        recent = sorted(combined,key=lambda obj: obj.timestamp, reverse=True)
    except Sale.DoesNotExist:
        recent = None
    return render(request, 'main/skin_detail.html', {'skin': skin,'recent':recent})


def skin_sale(request, sale_id):
    sale = Sale.objects.get(sale_id=sale_id)
    return render(request, 'main/skin_sale.html', {'sale': sale})

def skins(request):
    skins = Skin.objects.all()
    return render(request,'main/skins.html', {'skins': skins})

def user(request,username):
    user = User.objects.get(username=username)
    owned_skins = OwnedSkin.objects.filter(user=user)
    total_value = sum(owned_skin.skin.lbin * owned_skin.quantity for owned_skin in owned_skins)
    for owned_skin in owned_skins:
        owned_skin.value=(owned_skin.skin.lbin * owned_skin.quantity)
    return render(request, 'main/user_detail.html', {'user': user, 'owned_skins': owned_skins, 'total_value':total_value})

def search_skins(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', 'name')
    order = request.GET.get('order', 'false').lower() == 'true'
    skins = Skin.objects.filter(name__icontains=query) if query else Skin.objects.all()

    try:
        sort_by = f"-{sort_by}" if order else sort_by
        skins = skins.order_by(sort_by)
    except Exception as e:
        print(e)
        skins = skins.order_by('name')

    html = render_to_string('partials/skin_table_rows.html', {'skins': skins})
    return JsonResponse({'html': html})

