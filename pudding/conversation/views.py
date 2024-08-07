from django.shortcuts import redirect,render,get_object_or_404
from item.models import item as I
from django.contrib.auth.decorators import login_required
from .models import  Conversation
from .forms import  ConversationMesaageForm
@login_required()
def new_conversation(request,item_id):
    item=get_object_or_404(I,id=item_id)

    if item.created_by==request.user:
        return redirect('dashboard:index')

    conversations=Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('conversation:detail',id=conversations.first().id)

    if request.method=='POST':
        form=ConversationMesaageForm(request.POST)

        if form.is_valid():
            conversation=Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message=form.save(commit=False)
            conversation_message.conversation=conversation
            conversation_message.created_by=request.user
            conversation_message.save()
            return redirect('item:detail',id=item_id)
    else:
        form=ConversationMesaageForm()

    return render(request,
    'conversation/new.html',
    {
            "form":form,
            'title':'Inbox'
                  })

@login_required()
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request,'conversation/inbox.html',{"conversations":conversations})

@login_required()
def detail(request,id):
    conversation=Conversation.objects.filter(members__in=[request.user.id]).get(id=id)
    if request.method=="POST":

        form=ConversationMesaageForm(request.POST)
        if form.is_valid():
            conversation_message=form.save(commit=False)
            conversation_message.conversation=conversation
            conversation_message.created_by=request.user
            conversation_message.save()
            conversation.save()
            return redirect('conversation:detail',id=id)
    else:
        form=ConversationMesaageForm()
    return  render(request,
                   'conversation/conversation.html',
                   {"conversation":conversation,
                    "title":'Messages',
                    "form":form,
                    })