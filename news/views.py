import datetime as dt

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .email import send_welcome_email
from .forms import NewArticleForm, NewsLetterForm
from .models import Article, NewsLetterRecipients, WeshyMerch
from .permissions import IsAdminOrReadOnly
from .serializer import MerchSerializer


# Create your views here.
def news_today(request):
    date = dt.date.today()
    news = Article.today_news()
    form = NewsLetterForm()

    return render(request, 'all-news/today-news.html', {"date": date, "news_item":news, "form":form})

'''
We pass the serialize function which converts the form values into a JSON that will be passed into the request. 
If the AJAX request is successful, it will alert the user that it is successful. We then clear the form fields. 
Now when you submit that form you will see that the page will not reload but a welcome email will be sent.
'''

def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')

    recipient =  NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully added to mailing list'}
    return JsonResponse(data)


def past_days_news(request,past_date):
    try:
        # Converts data from the string Url
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
        assert False
    
    if date == dt.date.today():
        return redirect(news_today)
    
    news = Article.days_news(date)
    return render(request, 'all-news/past-news.html', {"date": date, "news":news})

def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html', {"message": message, "articles": searched_articles})

    else:
        message = "You haven't searched for any item"
        return render(request, 'all-news/search.html', {"message":message}) 

@login_required(login_url='/accounts/login/')
def article(request, article_id):
    try:
        article = Article.objects.get(id= article_id)
    except DoesNotExist:
        raise Http404

    return render(request, "all-news/article.html", {"article": article})

@login_required(login_url='/accounts/login/')
def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
        return redirect('newsToday')

    else:
        form = NewsLetterForm()
    return render(request, 'new_article.html', {"form": form})


def log_out(request):
    logout(request)
    return redirect(news_today)

class MerchList(APIView):
    def get(self, request, formart=None):
        all_merch = WeshyMerch.objects.all()
        serializers = MerchSerializer(all_merch, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = WeshyMerch(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = (IsAdminOrReadOnly)

class MerchDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    # Getting a single Item
    def get_merch(self, pk):
        try:
            return WeshyMerch.objects.get(pk=pk)
        except WeshyMerch.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = MerchSerializer(merch)
        return Response(serializers.data)

    # Update an object
    def put(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = MerchSerializer(merch, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    # Deleting an Object
    def delete(self, request, pk, format=None):
        merch = self.get_merch(pk)
        merch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        