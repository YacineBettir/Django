from django.shortcuts import redirect,render,get_object_or_404
from item.models import item
from .models import  Conversation
from .forms import  ConversationMesaageForm
def new_conversation(request,item_id):
    items=get_object_or_404(item,id=item_id)

    if items.created_by==request.user:
        return redirect('dashboard:index')

    conversations=Conversation.objects.filter(items=items).filter(member__in=[request.user.id])

    if conversations:
        pass

    if request.method=='POST':
        form=ConversationMesaageForm(request.POST)

        if form.is_valid():
            conversation=Conversation.objects.create(items=items)
            conversation.members.add(request.user)
            conversation.members.add(items.created_by)
            conversation.save()

            conversation_message=form.save(commit=False)
            conversation_message.conversation=conversation
            conversation_message.created_by=request.user
            conversation_message.save()
            return redirct('item:detail',id=item_id)
    else:
        form=ConversationMesaageForm()

    return render(request,'conversation/new.html',{"form":form,
                                                   'title':'Inbox'})
