from django.shortcuts import redirect,render,get_object_or_404
from .models import item,Category
from django.db.models import  Q
from .forms import NewItemForm,EditItemForm
from django.contrib.auth.decorators import login_required



def browse(request):
    query=request.GET.get('query','')
    category_id=request.GET.get('category',0)
    items=item.objects.filter(is_sold=False)
    categories=Category.objects.all()

    if category_id:
        items=items.filter(category_id=category_id)

    if query:
        items=items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context={
        "title":'Browse',
        "items":items,
        'query':query,
        "categories":categories,
        "category_id":int(category_id)
    }

    return   render(request,'item/browse.html',context=context)

def detail(request, id):
    items=get_object_or_404(item,id=id)
    related_items=item.objects.filter(category=items.category,is_sold=False).exclude(id=id)[0:3]
    context={
        'items':items,
        'related_items':related_items
    }
    return render(request,'item/details.html',context=context)
@login_required()
def newitem(request):
    if request.method=="POST":
        form=NewItemForm(request.POST,request.FILES)

        if form.is_valid():
            item=form.save(commit=False)
            item.created_by=request.user
            item.save()
            return redirect('item:detail',
                          id=item.id )
    else:
         form = NewItemForm()

    context={
            'form':form,
            'title':'New Item'
        }
    return render(request,
            'item/forms.html',
                  context=context
                  )
@login_required()
def delte_item(request,id):
    itm=get_object_or_404(item,id=id,created_by=request.user)
    itm.delete()
    return  redirect('dashboard:index')

def edititem(request,id):
    itm=get_object_or_404(item,id=id,created_by=request.user)

    if request.method=="POST":
        form=EditItemForm(request.POST,request.FILES,instance=itm)
        if form.is_valid():
            form.save()
            return redirect('item:detail',
                          id=itm.id )
    else:
         form = EditItemForm(instance=itm)
    context={
            'form':form,
            'title':'Edit Item'
        }
    return render(request,
            'item/forms.html',
                  context=context
                  )