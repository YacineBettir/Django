from django.shortcuts import render
from item.models import item
from django.contrib.auth.decorators import login_required



@login_required()
def index(request):
    items=item.objects.filter(created_by=request.user)

    return  render(request,
                   'dashboard/index.html',
                   {"items":items,
                        "title":'Dashboard'
                    }
                   )

