from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.utils import timezone

import re
from django.views.decorators.csrf import ensure_csrf_cookie
import requests as web
import bs4
import lxml
import random
from .words import WordsItem
from urllib.parse import urlparse
# Create your views here.


def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj




def index(request):
    words_list = WordsItem.words_list
    random_words = random.sample(words_list, 5)
    #random_page_words = random.sample(words_list, 5)
    #result_list = []
    #cleaner_list = []
    news_result_list = [] #
    news_cleaner_list = [] #
    tag_list = []
    #domain_list = []
    news_date_list = []
    #content_list = []
    news_domain_list = []
    news_content_list = []
    give_url_list = []
    for i in random_words:
        #page_url = 'https://www.google.com/search?num=3&q={}&source=lnms'.format(i)
        news_url = 'https://www.google.com/search?num=3&q={}&source=lnms&tbm=nws'.format(i)#
        give_url = 'https://www.google.com/search?q={}&source=lnms'.format(i)#
        #search = web.get(page_url)
        news_search = web.get(news_url)#
        #soup1 = bs4.BeautifulSoup(search.text, 'html.parser')
        try:
            soup2 = bs4.BeautifulSoup(news_search.text, 'lxml')
        except:
            soup2 = bs4.BeautifulSoup(news_search.text, 'html.parser')
        #title = soup1.select('.r > a')
        """if soup1.select('.slp > .f'):
            date = soup1.select('.slp > .f')
        else:
            date = ''"""
        #content = soup1.select('.st')
        news_title = soup2.select('.r > a')#
        news_date = soup2.select('.slp > .f')
        news_content = soup2.select('.st')
        news_link_list = []#
        news_domain_link_list = []
        #link_list = []
        """for t in title:
            title_text = t.getText()
            result_list.append(title_text)
            final_url = t.get('href')
            link_list.append(final_url)
            tag_list.append(i)"""

        for n in news_title:#
            news_text = n.getText()
            news_result_list.append(news_text)
            news_final_url = n.get('href')
            news_link_list.append(news_final_url)
            tag_list.append(i)
            give_url_list.append(give_url)
         
        """for l in link_list:
            l = l.replace('/url?q=','')
            l = l.split('&sa')[0]
            cleaner_list.append(l)"""

        for nl in news_link_list:#
            nl = nl.replace('/url?q=','')
            nl = nl.split('&sa')[0]
            news_cleaner_list.append(nl)
            news_domain_link_list.append(nl)

        """for d in cleaner_list:
            parsed_url = urlparse(d)
            domain = parsed_url.netloc
            domain_list.append(domain)"""

        for nd in news_date:
            nd = nd.getText()
            news_date_list.append(nd)

        """for c in content:
            c = c.getText()
            content_list.append(c)"""

        for ndl in news_domain_link_list:
            parsed_url = urlparse(ndl)
            news_domain = parsed_url.netloc
            news_domain_list.append(news_domain)

        for nc in news_content:
            nc = nc.getText()
            news_content_list.append(nc)

    """page_title = result_list
    page_link = cleaner_list
    page_domain = domain_list
    page_content = content_list"""
    news_title = news_result_list#
    news_link = news_cleaner_list#
    news_date = news_date_list
    news_domain = news_domain_list
    news_content = news_content_list
    give_url = give_url_list
    #pages = zip(page_title, page_link, tag_list, page_domain, page_content)
    news = zip(news_title, news_link, tag_list, news_date, news_content_list, give_url, news_domain)#

    return render(request, 'service/index.html', {'news':news,'random':random_words })


def crawl(request):
    if request.method == 'POST':
        if request.POST['keywords']:
            word = request.POST['keywords']
            initial_url = 'https://www.merriam-webster.com/thesaurus/{}'.format(word)
            search = web.get(initial_url)
            try:
                soup1 = bs4.BeautifulSoup(search.text, 'lxml')
            except:
                soup1 = bs4.BeautifulSoup(search.text, 'html.parser')
            text = soup1.select('.ant-list > .thes-list-content > p > a')
            if text == []:
                list = []
                list.append(word)
            else:
                list = []
                for t in text[:3]:
                    text = t.getText()
                    list.append(text)

            page_result_list = []
            page_cleaner_list = []
            page_domain_list = []
            page_content_list = []

            news_result_list = []
            news_cleaner_list = []
            news_date_list = []
            news_domain_list = []
            news_content_list = []

            for word in list:
                news_url = 'https://www.google.com/search?num=9&q={}&source=lnms&tbm=nws'.format(word)
                page_url = 'https://www.google.com/search?num=9&q={}&source=lnms'.format(word)
                news_search = web.get(news_url)
                news_soup = bs4.BeautifulSoup(news_search.text, 'html.parser')
                page_search = web.get(page_url)
                page_soup = bs4.BeautifulSoup(page_search.text, 'html.parser')

                news_title = news_soup.select('.r > a')#
                news_date = news_soup.select('.slp > .f')
                news_content = news_soup.select('.st')

                page_title = page_soup.select('.r > a')#
                page_content = page_soup.select('.st')

                page_link_list = []
                news_link_list = []

                news_domain_link_list = []
                page_domain_link_list = []

                for t in news_title:
                    text = t.getText()
                    news_result_list.append(text)
                    news_final_url = t.get('href')
                    news_link_list.append(news_final_url)
                
                for l in news_link_list:
                    l = l.replace('/url?q=','')
                    l = l.split('&sa')[0]
                    news_cleaner_list.append(l)
                    news_domain_link_list.append(l)

                for t in page_title:
                    text = t.getText()
                    page_result_list.append(text)
                    page_final_url = t.get('href')
                    page_link_list.append(page_final_url)
                
                for l in page_link_list:
                    l = l.replace('/url?q=','')
                    l = l.split('&sa')[0]
                    page_cleaner_list.append(l)
                    page_domain_link_list.append(l)

                for nd in news_date:
                    nd = nd.getText()
                    news_date_list.append(nd)

                for ndl in news_domain_link_list:
                    parsed_url = urlparse(ndl)
                    news_domain = parsed_url.netloc
                    news_domain_list.append(news_domain)

                for nc in news_content:
                    nc = nc.getText()
                    news_content_list.append(nc)

                for nc in page_content:
                    nc = nc.getText()
                    page_content_list.append(nc)

                for d in page_domain_link_list:
                    parsed_url = urlparse(d)
                    domain = parsed_url.netloc
                    page_domain_list.append(domain)

            news_title = news_result_list
            news_link = news_cleaner_list
            news_date = news_date_list
            news_domain = news_domain_list
            news_content = news_content_list
            news = zip(news_title, news_link, news_date, news_content, news_domain)

            page_title = page_result_list
            page_link = page_cleaner_list
            page_domain = page_domain_list
            page_content = page_content_list
            page = zip(page_title, page_link, page_domain, page_content)
            return render(request, 'service/result.html', {'news':news, 'page':page})

        else:
            return render(request, 'service/result.html', {'error': 'エラー'})
    else:
        pass

def tutorial(request):
    return render(request, 'service/about.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def logged_out_page(request):
    return render(request, 'accounts/logged_out.html')

def mypage(request):
    if request.method == 'POST':
        if 'save' in request.POST:
            current_user = request.user
            #user_id = current_user.id
            item = Item()
            item.account = current_user
            item_title = request.POST['item_title']
            item_link = request.POST['item_link']
            item_date_title = request.POST['item_date_title']
            item_keyword = request.POST['item_keyword']
            item_keyword_link = request.POST['item_keyword_link']

            item.title = item_title
            item.title_link = item_link
            item.date_title = item_date_title
            item.keyword = item_keyword
            item.keyword_link = item_keyword_link
            item.save()
            save_message = "the item successfully saved to your saved items!"
            try:
                saved_item = get_list_or_404(Item, account=current_user)
                saved_item = paginate_queryset(request, saved_item, 15)
            except:
                saved_item = None
            return render(request, 'service/mypage.html',{'saved_item':saved_item,'save_message':save_message})

        elif 'n_save' in request.POST:
            current_user = request.user
            #user_id = current_user.id
            item = Item()
            item.account = current_user
            item_title = request.POST['n_title']
            item_link = request.POST['n_link']
            item_date_title = request.POST['n_domain']

            item.title = item_title
            item.title_link = item_link
            item.date_title = item_date_title
            item.save()
            save_message = "the item successfully saved to your saved items!"
            try:
                saved_item = get_list_or_404(Item, account=current_user)
                saved_item = paginate_queryset(request, saved_item, 15)
            except:
                saved_item = None
            return render(request, 'service/mypage.html',{'saved_item':saved_item,'save_message':save_message})

        elif 'p_save' in request.POST:
            current_user = request.user
            #user_id = current_user.id
            item = Item()
            item.account = current_user
            item_title = request.POST['p_title']
            item_link = request.POST['p_link']
            item_date_title = request.POST['p_domain']

            item.title = item_title
            item.title_link = item_link
            item.date_title = item_date_title
            item.save()
            save_message = "the item successfully saved to your saved items!"
            try:
                saved_item = get_list_or_404(Item, account=current_user)
                saved_item = paginate_queryset(request, saved_item, 15)
            except:
                saved_item = None
            return render(request, 'service/mypage.html',{'saved_item':saved_item,'save_message':save_message})

        elif 'remove' in request.POST:
            current_user = request.user
            del_item_title = request.POST['del_item_title']
            del_item_link = request.POST['del_item_link']
            Item.objects.filter(account=current_user, title_link=del_item_link).delete()
            remove_message = "the item successfully removed from your saved items!"
            try:
                saved_item = get_list_or_404(Item, account=current_user)
                saved_item = paginate_queryset(request, saved_item, 15)
            except:
                saved_item = None
            return render(request, 'service/mypage.html',{'saved_item':saved_item,'remove_message':remove_message})
    current_user = request.user
    try:
        saved_item = get_list_or_404(Item, account=current_user)
        saved_item = paginate_queryset(request, saved_item, 15)
    except:
        saved_item = None
    return render(request, 'service/mypage.html',{'saved_item':saved_item})

def pre_quit(request):
    return render(request,'accounts/quit.html')

def quit(request):
    if request.method == 'POST':
        if 'quit' in request.POST:
            current_user = request.user
            Item.objects.filter(account=current_user).delete()
            User.objects.get(username = current_user.username).delete()
            return render(request, 'accounts/cu.html')

