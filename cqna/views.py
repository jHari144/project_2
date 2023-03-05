from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection, transaction
from django.utils import timezone
from django.views.decorators.cache import cache_control
from django.contrib import messages
import re
# Create your views here.

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def index(request):
#     #post is not recognised POST is correct
#     if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
#     #  print("fubuki atsuya")
#         return redirect("cqna:user_posts")
#     else:
#         cursor=connection.cursor()
#         val=(request.POST['num1'])
#         va=(request.POST['num2'])
#         rows=[]
     
#      #print(len(va)) it is empty thing
#         try:
#     #   print("&")
#             cursor.execute('''select password from users where id=%s'''%(val))
#             rows=cursor.fetchall()
#     #   print(rows)
#             if len(rows)!=0 and ((len(va)==0 and len(rows[0])==0) or (rows[0][0]==va)):
#     #    print("kalu")
#                 response= redirect("cqna:user_posts")
#                 response.set_cookie("UserID",val)
#                 response.set_cookie("login_status",True)
#                 request.session['logged_in'] = True
#                 request.session['user_id'] = val
#                 return response
#             else:
#                 messages.success(request,("Invalid UsedID/password"))
#                 return HttpResponse(render(request,'hello.html',{}))
#             cursor.close()
#         except Exception:
#             print("*")
#             messages.success(request,("Invalid UsedID/password"))
#             return HttpResponse(render(request,'hello.html',{}))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
    # if request.session.get('logged_in'):
        # print("kalu")
        return redirect("cqna:user_posts")
    else:
        if request.method == 'POST':
            # print("kalu2")
            val = request.POST.get('num1')
            va = request.POST.get('num2')
            if not val:
                error_message = 'Please enter user_id.'
                # print(error_message)
            elif not va:
                error_message = 'Please enter a password'
                # print(error_message)
            else:
                try:
                    val = int(val)
                    cursor = connection.cursor()
                    cursor.execute('''select password from users where id=%s'''%(val))
                    pas = cursor.fetchall()
                    cursor.close()
                    if pas:
                        pas = pas[0][0]
                        # print(pas)
                        response= redirect("cqna:user_posts")
                        response.set_cookie("UserID",val)
                        if va == pas:
                            response.set_cookie("login_status",True)
                            return response
                        else:
                            error_message = 'Invalid Password!!'
                    else:
                        error_message = 'User_id does not exist'
                except ValueError:
                    error_message = 'Invalid number entered.'
            context = {'error_message': error_message}
        else:
            context = {}
        # print(context)
        return render(request, 'hello.html', context)


# def index(request):
#     if request.session.get('logged_in'):
#         return redirect('cqna:user_posts')
#     if request.method == 'POST':
#         my_number_str = request.POST.get('my_number', '').strip()
#         my_password = request.POST.get('my_password', '').strip()
#         if not my_number_str:
        #     error_message = 'Please enter user_id.'
        # elif not my_password:
        #     error_message = 'Please enter a password'
#         else:
#             try:
#                 my_number = int(my_number_str)
#                 user_id = my_number
#                 cursor = connection.cursor()
#                 cursor.execute(''' select password from upass where user_id = %s '''%(user_id))
#                 pas = cursor.fetchall()
#                 cursor.close()
#                 if pas:
#                     pas = pas[0][0]
#                     request.session['user_id'] = user_id
#                     if my_password == pas:
#                         request.session['password'] = my_password
#                         request.session['logged_in'] = True
#                         return redirect('cqna:user_posts')
#                     else:
#                         error_message = 'Invalid Password!!'
#                 else:
#                     error_message = 'User_id does not exist'
#             except ValueError:
#                 error_message = 'Invalid number entered.'
#         context = {'error_message': error_message}
#     else:
#         context = {}
#     return render(request, 'cqna/index.html', context)

def fun(request):
 if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
    print("*???")
    return redirect("home")
 else:
    return render(request,'wait.html')

# def successregis(request):
#     if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
#         print("*???")
#         return redirect("home")
#     else:
#         if request.method == 'POST':
#             try:
#                 UserName = request.POST.get('')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def successregis(request):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        print("*???")
        return redirect("home")
    else:
        if request.method == 'POST':
            try:
                UserName = request.POST.get('UserName')
                print(UserName)
                #val2=request.POST['num2']
                Location = request.POST.get('Location')
                print(Location)
                WrbUrl = request.POST.get('WrbUrl')
                print(WrbUrl)
                AboutMe = request.POST.get('AboutMe')
                print(AboutMe)
                password = request.POST.get('password')
                print(password)
                if password == '':
                    message = 'Please Fill the password'
                    context = {'message': message}
                    #messages.success(request,("Invalid Details"))
                    return render(request, "wait.html", context)
                else:    
                    #val7=request.POST['num7']
                    #print(val7)
                    
                    # now=datetime.datetime.now()
                    now = timezone.localtime(timezone.now())
                    print(now)
        #here the real problem was '%s'
                    cursor=connection.cursor()
                    cursor.execute('''insert into users (display_name, reputation, location, website_url, about_me, creation_date, last_access_date, password) values(%s, 0, %s, %s, %s, %s, %s, %s) ''', [UserName, Location, WrbUrl, AboutMe, now, now, password])
                    transaction.commit()
                    cursor.execute('''select last_value from users_id_seq''')
                    value=cursor.fetchall()

                    context={
                        'UserID': value[0][0],
                        'password': password
                    }
                    print(value[0][0], password)
                    cursor.close()
                    return render(request, 'success.html', context)
            except Exception:
                message = 'Invalid Details'
                context = {'message': message}
                #messages.success(request,("Invalid Details"))
                return render(request, "wait.html", context)
        else:
            return render(request, 'wait.html')

def user_posts(request):
    # if request.session.get('logged_in'):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        user_id = int(request.COOKIES['UserID'])
        cursor = connection.cursor()
        cursor.execute(''' select title from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc'''%(user_id))
        val = cursor.fetchall()
        cursor.execute(''' select id from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc'''%(user_id))
        ids = cursor.fetchall()
        title_list = []
        id_list = []
        for v in val:
            title_list.append(v[0])

        for i in ids:
            id_list.append(i[0])
        
        data = []
        i = 0
        for id in id_list:
            data.append([id, title_list[i]])
            i = i+1

        context = {'data': data, 'user_id': user_id}
        
        cursor.close()
        
        return render(request, 'cqna/user_posts.html', context)

    else:
        context = {}
        return render(request, 'hello.html', context)

def split_tags_list(tag_string):
    tags = []
    fin_tags = []
    tags = tag_string.split('<')[1:]
    for b in tags:
        fin_tags.append(b.split('>')[0])
    return fin_tags

def make_tags_str(tags):
    if tags:
        tag_str = '<'
        for a in tags[:-1]:
            tag_str = tag_str + a + '><'
        tag_str = tag_str + tags[-1] + '>'
    else:
        tag_str = ''
    return tag_str

def tag_check(tag):
    cursor = connection.cursor()
    cursor.execute(''' select tag_name from tags where tag_name = %s ''', [tag])
    tag_name = cursor.fetchall()
    cursor.close()
    if tag_name:
        return True
    else:
        return False

def detail(request, post_id):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        u_id = int(request.COOKIES['UserID'])
        # print(type(u_id))
        cursor = connection.cursor()
        cursor.execute(''' select owner_user_id from posts where id = %s ''', [post_id])
        owner_id = cursor.fetchall()[0][0]
        cursor.execute(''' select title from posts where post_type_id = 1 and id = %s order by creation_date desc ''', [post_id])
        post_title = cursor.fetchall()[0][0]
        cursor.execute(''' select body from posts where post_type_id = 1 and id = %s order by creation_date desc ''', [post_id])
        body = cursor.fetchall()[0][0]
        cursor.execute(''' select tags from posts where post_type_id = 1 and id = %s order by creation_date desc ''', [post_id])
        tag_str = cursor.fetchall()[0][0]
        if tag_str:
            tags = split_tags_list(tag_str)
        else:
            tags = None
        cursor.execute(''' select owner_user_id from posts where parent_id=%s order by id desc ''', [post_id])
        rid = cursor.fetchall()
        is_owner = (u_id == owner_id)
        r_id_fin = []
        for i in rid:
            if i[0] == None:
                r_id_fin.append('Anonymous')
            else:
                r_id_fin.append(i[0])
        
        cursor.execute(''' select body from posts where parent_id=%s order by id desc ''', [post_id])
        bod = cursor.fetchall()
        bod_fin = []
        for i in bod:
            bod_fin.append(i[0])
        Replies = []
        i = 0
        for id in r_id_fin:
            Replies.append([id, bod_fin[i]])
            i = i+1
        context = {'is_owner': is_owner, 'u_id': owner_id ,'post_title': post_title, 'body': body, 'tags': tags, 'Replies': Replies, 'post_id': post_id}
        return render(request, 'cqna/detail.html', context)
    else:
        context = {}
        return render(request, 'hello.html', context)

def reply(request, post_id):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        u_id = int(request.COOKIES['UserID'])
        cursor = connection.cursor()
        reply=None
        cursor.execute(''' select title from posts where post_type_id = 1 and id = %s order by creation_date desc ''', [post_id])
        post_title = cursor.fetchall()[0][0]
        cursor.execute(''' select body from posts where post_type_id = 1 and id = %s order by creation_date desc ''', [post_id])
        body = cursor.fetchall()[0][0]
        cursor.execute(''' select tags from posts where post_type_id = 1 and id = %s order by creation_date desc ''', [post_id])
        tag_str = cursor.fetchall()[0][0]
        if tag_str:
            tags = split_tags_list(tag_str)
        else:
            tags = None
        cursor.close()
        if request.method == 'POST':
            if request.POST.get('reply_text'):
                cursor = connection.cursor()
                creation_date = timezone.localtime(timezone.now())
                reply_text = request.POST.get('reply_text')
                cursor.execute(''' insert into posts (owner_user_id, parent_id, post_type_id, body, creation_date) values(%s, %s, 2, %s, %s) ''', [u_id, post_id, reply_text, creation_date])
                transaction.commit()
                return redirect('cqna:detail', post_id)
            else:
                message = "Please fill in all the required fields."
                context = {'post_id': post_id, 'post_title': post_title, 'body':body, 'message': message, 'tags': tags}
                return render(request, 'cqna/reply.html', context)
        else:
            context = {'post_id': post_id, 'post_title': post_title, 'body':body, 'tags': tags}
            return render(request, 'cqna/reply.html', context)
    else:
        context = {}
        return render(request, 'hello.html', context)

def create_post(request):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        if request.method == 'POST':
            if request.POST.get('post_title') and request.POST.get('post_text'):
                request.session['tags'] = []
                user_id = int(request.COOKIES['UserID'])
                post_title = request.POST.get('post_title')
                post_body = request.POST.get('post_text')
                post_body = '<p>' + post_body +'</p>'
                post_body = post_body.replace('\n', '</p><p>')
                creation_date = timezone.localtime(timezone.now())
                cursor = connection.cursor()
                cursor.execute('''Insert into posts (owner_user_id, post_type_id, view_count, answer_count, title, body, creation_date) values( %s, 1, 0, 0, %s, %s, %s)''', [user_id, post_title, post_body, creation_date])
                transaction.commit()
                return redirect('cqna:add_tags')
            else:
                message = "Please fill in all required fields."
                return render(request, 'cqna/create_post.html', {'message': message})
        else:
            return render(request, 'cqna/create_post.html')
    else:
        context = {}
        return render(request, 'hello.html', context)

def search_tag_in(tags):
    if len(tags) != 0:
        cursor = connection.cursor()
        cursor.execute(''' select tags from posts where post_type_id = 1 order by creation_date desc, score desc ''')
        rset_tags = cursor.fetchall()
        tags_arr = []
        for a in rset_tags:
            tags_arr.append(a[0])
        
        n_tags_arr = []
        
        for a in tags_arr:
            if a:
                n_tags_arr.append(split_tags_list(a))
            else:
                n_tags_arr.append(None)

        cursor.execute(''' select id from posts where post_type_id = 1 order by creation_date desc, score desc ''')
        rset_id = cursor.fetchall()
    
        id_arr = []

        for a in rset_id:
            id_arr.append(a[0])

        cursor.execute(''' select count(*) from posts where post_type_id = 1 ''')
        count = cursor.fetchall()[0][0]
    
        pos_count = list(range(count))
    
        n_pos = []
    
        for t in tags:
            n_pos = pos_count.copy()
            pos_count = []
            for i in n_pos:
                if n_tags_arr[i]:
                    for in_tag in n_tags_arr[i]:
                        if in_tag == t:
                            pos_count.append(i)
            n_pos = []

        cursor.execute(''' select title from posts where post_type_id = 1 order by creation_date desc, score desc ''')
        rset_title = cursor.fetchall()
        title_arr = []
        for a in rset_title:
            title_arr.append(a[0])

        id_title = [] 

        for i in pos_count:
            id_title.append([id_arr[i], title_arr[i]])
        cursor.close()
        return id_title
    else:
        return []

def search_tag(request):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        if request.method=='POST':
            if 'done' in request.POST:
                if request.POST.get('tag') != '':
                    try:
                        tags = request.session.get('tags')
                        tag = request.POST.get('tag', '').strip()
                        if tag_check(tag) and tag not in tags:
                            tags.append(tag)
                            request.session['tags'] = []
                            id_title = search_tag_in(tags)
                            return search_detail(request, id_title, 1, tags)
                        elif tag in tags:
                            error_message = 'Tag already chosen'
                            context = {'error_message': error_message, 'tags': tags}
                        else:
                            error_message = 'Select valid tag!'
                            context = {'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {}
                else:
                    try:
                        tags = request.session.get('tags')
                        request.session['tags'] = []
                        id_title = search_tag_in(tags)
                        if len(id_title) != 0:
                            return search_detail(request, id_title, 1, tags)
                        else:
                            error_message = 'Select tag!'
                            context = {'error_message': error_message, 'tags': tags}
                        #return search_detail(request, id_title, 1, tags)
                    except ValueError:
                        context = {}
                return render(request, 'cqna/search_tag.html', context)
            elif 'add' in request.POST:
                if request.POST.get('tag') != '':
                    try:
                        tags = request.session.get('tags')
                        tag = request.POST.get('tag', '').strip()
                        if tag_check(tag) and tag not in tags:
                            tags.append(tag)
                            context={'tags': tags}
                            request.session['tags'] = tags
                        elif tag in tags:
                            error_message = 'Tag already chosen'
                            context = {'error_message': error_message, 'tags': tags}
                        else:
                            error_message = 'Select valid tag!'
                            context = {'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {}
                    return render(request, 'cqna/search_tag.html', context)
                else:
                    try:
                        tags = request.session.get('tags')
                        error_message = 'Select tag!'
                        context = {'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {}
                    return render(request, 'cqna/search_tag.html', context)
            else:
                context = {}
                return render(request, 'cqna/search_tag.html', context)
        else:  
            context = {}
            return render(request, 'cqna/search_tag.html', context)
    else:
        context = {}
        return render(request, 'hello.html', context)

def search_user(request):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        if request.method == 'POST':
            s_user = int(request.POST.get('s_user'))
            # print(s_user, 'hellalujash')
            if s_user:
                cursor = connection.cursor()
                cursor.execute(''' select id from users where id = %s ''', [s_user])
                id_exist = cursor.fetchall()
                if id_exist:
                    cursor = connection.cursor()
                    cursor.execute(''' select id from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc, score desc ''', [s_user])
                    rset_id = cursor.fetchall()
                    rs_id = []
                    for a in rset_id:
                        rs_id.append(a[0])

                    cursor.execute(''' select title from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc, score desc ''', [s_user])
                    rset_title = cursor.fetchall()
                    rs_title = []
                    for a in rset_title:
                        rs_title.append(a[0])

                    id_title = []
                    i = 0
                    for a in rs_id:
                        id_title.append([a, rs_title[i]])
                        i += 1

                    return search_detail(request, id_title, 2, s_user)
                else:
                    error_message = 'Selected user does not exist!'
                    context = {'error_message': error_message}
                    return render(request, 'cqna/search_user.html', context)
            else:
                error_message = 'Select user properly!'
                context = {'error_message': error_message}
                return render(request, 'cqna/search_user.html', context)
        else:
            return render(request, 'cqna/search_user.html', {})
    else:
        context = {}
        return render(request, 'hello.html', context)

def search_detail(request, id_title, type, q):
    if id_title:
        if type == 1:
            tags = q
            tag = True
            context = {'tag': tag, 'tags': tags, 'id_title': id_title}
        elif type == 2:
            s_user = q
            context = {'s_user': s_user, 'id_title': id_title}
    else:
        if type == 1:
            tags = q
            tag = True
            message= "No posts with such tags"
            context = {'message': message, 'tag': tag, 'tags': tags}
        if type == 2:
            s_user = q
            message = "User_{} has no posts yet".format(s_user)
            context = {'message': message, 's_user': s_user}
    return render(request, 'cqna/search_detail.html', context)


def call_search(request):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        return render(request, 'cqna/search.html')
    else:
        context = {}
        return render(request, 'hello.html', context)

def edit_post(request, post_id):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        cursor = connection.cursor()
        cursor.execute(''' select title from posts where id = %s ''', [post_id])
        title = cursor.fetchall()[0][0]
        cursor.execute(''' select body from posts where id = %s ''', [post_id])
        body = cursor.fetchall()[0][0]
        body = re.sub(r'<p>', '', body)
        body = re.sub(r'</p>', '\n', body)
        cursor.close()
        if request.method == 'POST':
            if request.POST['post_title'] and request.POST['post_text']:
                post_title = request.POST.get('post_title')
                post_text = request.POST.get('post_text')
                post_text = '<p>' + post_text +'</p>'
                post_text = post_text.replace('\n', '</p><p>')
                edit_time = timezone.localtime(timezone.now())
                cursor = connection.cursor()
                cursor.execute(''' update posts set title = %s, body = %s, last_edit_date = %s where id = %s ''', [post_title, post_text, edit_time, post_id])
                transaction.commit()
                cursor.close()
                return redirect('cqna:edit_tags', post_id)
            else:
                message = "Please fill in all required fields."
                return render(request, 'cqna/edit_post.html', {'title': title, 'body': body, 'message': message, 'post_id': post_id})
        else:
            context = {'title': title, 'body': body, 'post_id': post_id}
            return render(request, 'cqna/edit_post.html', context)
    else:
        context = {}
        return render(request, 'hello.html', context)

def edit_tags(request, post_id):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        cursor = connection.cursor()
        cursor.execute(''' select tags from posts where id = %s ''', [post_id])
        pre_tags_str = cursor.fetchall()[0][0]
        cursor.close()
        # print(pre_tags_str)
        if pre_tags_str != None:
            pre_tags = split_tags_list(pre_tags_str)
        else:
            pre_tags = None
        if request.method=='POST':
            if 'done' in request.POST:
                if request.POST.get('tag') != '':
                    try:
                        tags = request.session.get('tags')
                        tag = request.POST.get('tag', '').strip()
                        if tag_check(tag) and tag not in tags:
                            cursor = connection.cursor()
                            tags.append(tag)
                            request.session['tags'] = []
                            p_id = post_id
                            t_string = make_tags_str(tags)
                            cursor.execute(''' update posts set tags = %s where id = %s ''', [t_string, p_id])
                            transaction.commit()
                            cursor.close()
                            pre_tags = []
                            return redirect('cqna:user_posts')
                        elif tag in tags:
                            error_message = 'Tag already chosen'
                            context = {'pre_tags': pre_tags, 'error_message': error_message, 'tags': tags}
                        else:
                            error_message = 'Select valid tag!'
                            context = {'pre_tags': pre_tags, 'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {'pre_tags': pre_tags}
                else:
                    try:
                        tags = request.session.get('tags')
                        request.session['tags'] = []
                        cursor = connection.cursor()
                        p_id = post_id
                        t_string = make_tags_str(tags)
                        cursor.execute(''' update posts set tags = %s where id = %s ''', [t_string, p_id])
                        transaction.commit()
                        pre_tags = []
                        cursor.close()
                        return redirect('cqna:user_posts')
                    except ValueError:
                        context = {'pre_tags': pre_tags}
                return render(request, 'cqna/edit_tags.html', context)
            elif 'add' in request.POST:
                if request.POST.get('tag') != '':
                    try:
                        tags = request.session.get('tags')
                        tag = request.POST.get('tag', '').strip()
                        if tag_check(tag) and tag not in tags:
                            tags.append(tag)
                            context={'pre_tags': pre_tags, 'tags': tags}
                            request.session['tags'] = tags
                        elif tag in tags:
                            error_message = 'Tag already chosen'
                            context = {'pre_tags': pre_tags, 'error_message': error_message, 'tags': tags}
                        else:
                            error_message = 'Select valid tag!'
                            context = {'pre_tags': pre_tags, 'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {'pre_tags': pre_tags}
                    return render(request, 'cqna/edit_tags.html', context)
                else:
                    try:
                        tags = request.session.get('tags')
                        error_message = 'Select tag!'
                        context = {'pre_tags': pre_tags, 'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {'pre_tags': pre_tags}
                    return render(request, 'cqna/edit_tags.html', context)
            elif 'cancel' in request.POST:
                return detail(request, post_id)
            else:
                context = {'pre_tags': pre_tags}
                return render(request, 'cqna/edit_tags.html', context)
        else:
            context = {'pre_tags': pre_tags}
            return render(request, 'cqna/edit_tags.html', context)
    else:
        context = {}
        return render(request, 'hello.html', context)

def delete_post(request, post_id):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        cursor = connection.cursor()
        cursor.execute(''' delete from posts where id = %s ''', [post_id])
        transaction.commit()
        cursor.close()
        return redirect('cqna:user_posts')
    else:
        context = {}
        return render(request, 'hello.html', context)

def add_tags(request):
    if 'login_status' in request.COOKIES and 'UserID' in request.COOKIES:
        if request.method=='POST':
            if 'done' in request.POST:
                if request.POST.get('tag') != '':
                    try:
                        tags = request.session.get('tags')
                        tag = request.POST.get('tag', '').strip()
                        if tag_check(tag) and tag not in tags:
                            cursor = connection.cursor()
                            tags.append(tag)
                            request.session['tags'] = []
                            cursor.execute(''' select id from posts order by id desc limit 1 ''')
                            p_id = cursor.fetchall()[0][0]
                            t_string = make_tags_str(tags)
                            cursor.execute(''' update posts set tags = %s where id = %s ''', [t_string, p_id])
                            transaction.commit()
                            cursor.close()
                            return redirect('cqna:user_posts')
                        elif tag in tags:
                            error_message = 'Tag already chosen'
                            context = {'error_message': error_message, 'tags': tags}
                        else:
                            error_message = 'Select valid tag!'
                            context = {'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {}
                else:
                    try:
                        tags = request.session.get('tags')
                        request.session['tags'] = []
                        cursor = connection.cursor()
                        cursor.execute(''' select id from posts order by id desc limit 1 ''')
                        p_id = cursor.fetchall()[0][0]
                        t_string = make_tags_str(tags)
                        cursor.execute(''' update posts set tags = %s where id = %s ''', [t_string, p_id])
                        transaction.commit()
                        cursor.close()
                        return redirect('cqna:user_posts')
                    except ValueError:
                        context = {}
                return render(request, 'cqna/add_tags.html', context)
            elif 'add' in request.POST:
                if request.POST.get('tag') != '':
                    try:
                        tags = request.session.get('tags')
                        tag = request.POST.get('tag', '').strip()
                        if tag_check(tag) and tag not in tags:
                            tags.append(tag)
                            context={'tags': tags}
                            request.session['tags'] = tags
                        elif tag in tags:
                            error_message = 'Tag already chosen'
                            context = {'error_message': error_message, 'tags': tags}
                        else:
                            error_message = 'Select valid tag!'
                            context = {'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {}
                    return render(request, 'cqna/add_tags.html', context)
                else:
                    try:
                        tags = request.session.get('tags')
                        error_message = 'Select tag!'
                        context = {'error_message': error_message, 'tags': tags}
                    except ValueError:
                        context = {}
                    return render(request, 'cqna/add_tags.html', context)
            else:
                context = {}
                return render(request, 'cqna/add_tags.html', context)
        else:  
            context = {}
            return render(request, 'cqna/add_tags.html', context)
    else:
        context = {}
        return render(request, 'hello.html', context)


def logout(request):
    request.session['tags'] = []
    response=redirect('cqna:user_posts')
    response.delete_cookie('UserID')
    response.delete_cookie('login_status')
    return response
