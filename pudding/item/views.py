from django.shortcuts import render,get_object_or_404
from .models import item
def detail(request, id):
    items=get_object_or_404(item,id=id)
    related_items=item.objects.filter(category=items.category,is_sold=False).exclude(id=id)[0:3]
    context={
        'items':items,
        'related_items':related_items
    }
    return render(request,'item/details.html',context=context)


