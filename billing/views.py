from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import simplejson

from .forms import CardForm


@login_required
def add_card(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        # convert the POST variables into JSON format
        post_data.__delitem__('csrfmiddlewaretoken')
        json_data = simplejson.dumps(post_data)

        # store the newly encrypted data as a Card instance
        form = CardForm(post_data)
        card = form.save(commit=False)
        card.user = request.user
        card.num = post_data.get('card_number')[-4:]
        card.save()
    else:
        form = CardForm()
    return render(request, "billing/add_card.html", locals())
