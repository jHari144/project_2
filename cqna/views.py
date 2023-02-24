from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection, transaction
from django.utils import timezone
# Create your views here.

def index(request):
    if request.session.get('logged_in'):
        return redirect('cqna:user_posts')
    if request.method == 'POST':
        my_number_str = request.POST.get('my_number', '').strip()
        my_password = request.POST.get('my_password', '').strip()
        if not my_number_str:
            error_message = 'Please enter user_id.'
        elif not my_password:
            error_message = 'Please enter a password'
        else:
            try:
                my_number = int(my_number_str)
                user_id = my_number
                cursor = connection.cursor()
                cursor.execute(''' select password from upass where user_id = %s '''%(user_id))
                pas = cursor.fetchall()
                cursor.close()
                if pas:
                    pas = pas[0][0]
                    request.session['user_id'] = user_id
                    if my_password == pas:
                        request.session['password'] = my_password
                        request.session['logged_in'] = True
                        return redirect('cqna:user_posts')
                    else:
                        error_message = 'Invalid Password!!'
                else:
                    error_message = 'User_id does not exist'
            except ValueError:
                error_message = 'Invalid number entered.'
        context = {'error_message': error_message}
    else:
        context = {}
    return render(request, 'cqna/index.html', context)

def user_posts(request):
    user_id = request.session.get('user_id')
    if request.session.get('logged_in'):
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
        return render(request, 'cqna/index.html', context)

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
    if request.session.get('logged_in'):
        u_id = request.session.get('user_id')
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
        return render(request, 'cqna/index.html', context)

def reply(request, post_id):
    if request.session.get('logged_in'):
        u_id = request.session.get('user_id')
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
        return render(request, 'cqna/index.html', context)

def create_post(request):
    if request.session.get('logged_in'): 
        if request.method == 'POST':
            if request.POST.get('post_title') and request.POST.get('post_text'):
                request.session['tags'] = []
                user_id = request.session.get('user_id')
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
        return render(request, 'cqna/index.html', context)

def search_tag_in(tags):
    if len(tags) != 0:
        cursor = connection.cursor()
        cursor.execute(''' select tags from posts order by creation_date desc ''')
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

        cursor.execute(''' select id from posts order by creation_date desc ''')
        rset_id = cursor.fetchall()
    
        id_arr = []

        for a in rset_id:
            id_arr.append(a[0])

        cursor.execute(''' select count(*) from posts ''')
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

        cursor.execute(''' select title from posts order by creation_date desc ''')
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
    if request.session.get('logged_in'):
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
                            if id_title:
                                context = {'id_title': id_title}
                            else:
                                message= "No posts with such tags"
                                context = {'message': message}
                            return render(request, 'cqna/search_detail.html', context)    
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
                        if id_title:
                            context = {'id_title': id_title}
                        else:
                            message= "No posts with such tags"
                            context = {'message': message}
                        return render(request, 'cqna/search_detail.html', context)
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
        return render(request, 'cqna/index.html', context)

def search_user(request):
    if request.session.get('logged_in'):
        if request.method == 'POST':
            s_user = request.POST.get('s_user')
            cursor = connection.cursor()
            cursor.execute(''' select id from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc''', [s_user])
            rset_id = cursor.fetchall()
            rs_id = []
            for a in rset_id:
                rs_id.append(a[0])

            cursor.execute(''' select title from posts where owner_user_id = %s and post_type_id = 1 order by creation_date desc ''', [s_user])
            rset_title = cursor.fetchall()
            rs_title = []
            for a in rset_title:
                rs_title.append(a[0])

            id_title = []
            i = 0
            for a in rs_id:
                id_title.append([a, rs_title[i]])
                i += 1

            context = {'id_title': id_title}

            return render(request, 'cqna/search_detail.html', context)
        else:
            return render(request, 'cqna/search_user.html', {})
    else:
        context = {}
        return render(request, 'cqna/index.html', context)

def call_search(request):
    return render(request, 'cqna/search.html')

def edit_post(request, post_id):
    if request.session.get('logged_in'):
        cursor = connection.cursor()
        cursor.execute(''' select title from posts where id = %s ''', [post_id])
        title = cursor.fetchall()[0][0]
        cursor.execute(''' select body from posts where id = %s ''', [post_id])
        body = cursor.fetchall()[0][0]
        cursor.close()
        if request.method == 'POST':
            if request.POST['post_title'] and request.POST['post_text']:
                post_title = request.POST.get('post_title')
                post_text = request.POST.get('post_text')
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
        return render(request, 'cqna/index.html', context)

def edit_tags(request, post_id):
    if request.session.get('logged_in'):
        cursor = connection.cursor()
        cursor.execute(''' select tags from posts where id = %s ''', [post_id])
        pre_tags_str = cursor.fetchall()[0][0]
        cursor.close()
        pre_tags = split_tags_list(pre_tags_str)
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
            else:
                context = {'pre_tags': pre_tags}
                return render(request, 'cqna/edit_tags.html', context)
        else:
            context = {'pre_tags': pre_tags}
            return render(request, 'cqna/edit_tags.html', context)
    else:
        context = {}
        return render(request, 'cqna/index.html', context)

def delete_post(request, post_id):
    if request.session.get('logged_in'):
        cursor = connection.cursor()
        cursor.execute(''' delete from posts where id = %s ''', [post_id])
        transaction.commit()
        cursor.close()
        return redirect('cqna:user_posts')
    else:
        context = {}
        return render(request, 'cqna/index.html', context)

def add_tags(request):
    if request.session.get('logged_in'):
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
        return render(request, 'cqna/index.html', context)


def logout(request):
    request.session['password'] = None
    request.session['user_id'] = None
    request.session['logged_in'] = False
    request.session['tags'] = []
    return redirect('cqna:user_posts')
