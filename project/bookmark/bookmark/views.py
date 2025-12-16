from django.http import Http404
from django.shortcuts import render, get_object_or_404

from bookmark.models import Bookmark


def bookmark_list(request):
    # 전체 리스트 보여주기
    # bookmarks = Bookmark.objects.all()

    # id가 50 이상인것만 보여주기
    bookmarks = Bookmark.objects.filter(id__gte=50)

    context = {'bookmarks': bookmarks}
    return render(request, 'bookmark_list.html', context)

def bookmark_detail(request, pk):
    # try:
    #     bookmark = Bookmark.objects.get(pk=pk)
    # except Bookmark.DoesNotExist:
    #     raise Http404

    bookmark = get_object_or_404(Bookmark, pk=pk)

    context = {'bookmark': bookmark}
    return render(request, 'bookmark_detail.html', context)
