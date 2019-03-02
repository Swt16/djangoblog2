from django import forms
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone
from myblog.forms import MyPostForm
from myblog.models import Post


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")


def list_view(request):
    published = Post.objects.exclude(published_date__exact=None)
    posts = published.order_by('-published_date')
    context = {'posts': posts}
    return render(request, 'list.html', context)


def detail_view(request, post_id):
    published = Post.objects.exclude(published_date__exact=None)
    try:
        post = published.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404
    context = {'post': post}
    return render(request, 'detail.html', context)


def edit_view(request, post_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(settings.LOGIN_URL)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = MyPostForm(request.POST, instance=post)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return HttpResponseRedirect('/posts/{}'.format(post_id))
    else:
        form = MyPostForm(instance=post)
        context = {'form': form, 'post': post}
        return render(request, "my_post.html", context)
