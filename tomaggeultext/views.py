from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Subscription, TMSeries, TMText, Comment
from .models import Genre
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Count
import math
import json


# Create your views here.
def tmtext(request):
    all_tmtext = TMText.objects.all().order_by('-date_of_write')
    popular_tmts = TMText.objects.annotate(like_num=Count('like_users')).order_by('-like_num')[:5] # 좋아요 많은 순으로 5개 
    print(popular_tmts)
    all_genre = Genre.objects.all()
    
    paginator = Paginator(all_tmtext,5)
    page=1 if(request.GET.get('page') == None) else int(request.GET.get('page'))
    posts = paginator.get_page(page)
    page_range = 5 #페이지 범위 지정 예 1, 2, 3, 4, 5 / 6, 7, 8, 9, 10
    current_block = math.ceil(page/page_range) #해당 페이지가 몇번째 블럭인가
    start_block = (current_block-1) * page_range
    end_block = start_block + page_range
    p_range = paginator.page_range[start_block:end_block]
    return render(request, 'mainpage.html', {'p_range':p_range , 'page': page,'posts':posts,'popular_tmts':popular_tmts, 'all_genre':all_genre})

def tmlist(request, pk):
    user = request.user
    series = get_object_or_404(TMSeries, series_id = pk)
    isSubs = False
    if user.is_authenticated:
        isSubs = user.subs.filter(tmseries=series)
    return render(request, 'tomaggeullist.html', {'series':series, 'isSubs':isSubs})

def popup(request):
    return render(request, 'popup.html')
    
@login_required
def it_sounds_good(request,tmt_id): # test
    user = request.user
    tmtext=TMText.objects.get(text_id=tmt_id)

    if tmtext.like_users.filter(email=user.email).exists():
        tmtext.like_users.remove(user)
    else:
        tmtext.like_users.add(user)
    tmtext.save()
    context = {'heart_count' : tmtext.heart_num}
    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
def subscribe(request,series): # test
    user = request.user
    tmseries = get_object_or_404(TMSeries, series_id=series)
    subs = user.subs.filter(tmseries=series)
    state = "구독 취소되었습니다."
    if subs:
        subs.delete()
    else:
        subs = Subscription(tmuser = user, tmseries = tmseries)
        subs.save()
        state = "구독 신청하였습니다."
    context = {'substext' : state}
    
    return HttpResponse(json.dumps(context), content_type='application/json')

def tmtext_detail(request, tmt_id):
    tmtext=get_object_or_404(TMText, text_id=tmt_id)
    if request.method == 'POST':
        isDelete = request.POST.get('id',None)
        if not isDelete:
            comment = request.POST.get('comment','')
            cmt = Comment(comment_content=comment, tmtext = tmtext, tmuser = request.user)
            cmt.save()
        else:
            Comment.objects.get(id=isDelete).delete()


        return redirect('tmtext_detail', tmtext.text_id)

    return render(request, 'tomaggeul_detail.html', {'tmtext':tmtext})
