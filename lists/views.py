from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from lists.forms import ItemForm, ExistingListItemForm
from lists.models import Item, List


def home_page(request):
    """Домашняя страница"""
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request, list_id):
    """Представление списка"""
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, "list.html", {"list": list_, "form": form})


def new_list(request):
    """Новый список"""
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, "home.html", {"form": form})


def my_lists(request, email):
    return render(request, 'my_lists.html')
