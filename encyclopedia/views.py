from cmath import e
from email import contentmanager
from pydoc import HTMLDoc
import random
from turtle import title
from django import forms
from django.shortcuts import redirect, render
from . import util
from markdown2 import Markdown

entries_list = util.list_entries()
markdowner = Markdown()

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    data = forms.CharField(widget=forms.Textarea(attrs={"rows":1, "cols":10}))

class EditEntryForm(forms.Form):
    title = forms.CharField(label = "title")
    body = forms.CharField(label="body", widget=forms.Textarea(attrs={'rows':1,'cols':10}))

class SearchEntryForm(forms.Form):
    query = forms.CharField(max_length=100)

def index(request):
    form = SearchEntryForm()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":form
    })
def search(request):

    if request.POST:
        form = SearchEntryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get("query")
            present = False
            for entry in util.list_entries():
                if data == entry:
                    mdcontent = util.get_entry(data)
                    htmlcontent = markdowner.convert(mdcontent)
                    present = True
                    break
            if present:
                return render(request,"encyclopedia/show_entry.html", {
                    "title":data,
                    "entry":htmlcontent,
                    "form":form
                })
            else:
                similarEntry = []
                for entry in util.list_entries():
                    if data in entry:
                        similarEntry.append(entry)
                if len(similarEntry) == 0:
                    form = SearchEntryForm()
                    content = "Page Not Found!"
                    return render(request,"encyclopedia/errorMsg.html",{
                        'form':form, "content":content
                    })
                else:
                    return render(request, "encyclopedia/index.html",{
                        "entries":similarEntry,
                        "form":form
                    })
    return None

def show_entry(request,title):
    form = SearchEntryForm()
    mdcontent = util.get_entry(title)
    htmlcontent = markdowner.convert(mdcontent)
    return render(request,"encyclopedia/show_entry.html", {
        "entry":htmlcontent, "title" : title, "form":form
    })

def edit_entry(request,title):
    form = SearchEntryForm()
    if request.POST:       
        editEntryForm = EditEntryForm(request.POST)
        if editEntryForm.is_valid():
            title = editEntryForm.cleaned_data.get("title")
            body = editEntryForm.cleaned_data.get("body")
            util.save_entry(title,body)
            htmlContent = markdowner.convert(body)
            return render(request,"encyclopedia/show_entry.html", {
                "title" : title, "entry":htmlContent
            })
    else:
        editform = EditEntryForm({"title":title, "body": util.get_entry(title)})
        return render(request, "encyclopedia/edit_entry.html", {
            "editform" : editform, "form":form
        })

def random_entry(request):
    form = SearchEntryForm()
    title = random.choice(entries_list)
    return render(request,"encyclopedia/show_entry.html", {
        "entry":util.get_entry(title),
        "title":title,
        "form":form
    })
def add_entry(request):
    form = SearchEntryForm()
    addform = NewEntryForm(request.POST)
    if request.method.POST:
        
        if form.is_valid():
            title = addform.cleaned_data["title"].replace(" ","")
            data = addform.cleaned_data["data"]
            util.save_entry(title,data)
            return redirect("index")
        else:
            return render(request,"encyclopedia/add_entry.html", {
                "addform":addform, "form":form
            })
    else:
        return render(request,"encyclopedia/add_entry.html",{
            "addform":addform, "form":form
        })