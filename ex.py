from django.db import connection, transaction

def split_tags_list(tag_string):
    tags = []
    fin_tags = []
    tags = tag_string.split('<')[1:]
    for b in tags:
        fin_tags.append(b.split('>')[0])
    return fin_tags

def search_tag_in(tags):
    cursor = connection.cursor()
    cursor.execute(''' select tags from posts ''')
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

    cursor.execute(''' select id from posts ''')
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

    cursor.execute(''' select title from posts ''')

    rset_title = cursor.fetchall()
    title_arr = []
    for a in rset_title:
        title_arr.append(a[0])
    id_tag_title_bod = [id_arr, title_arr]
    return id_tag_title_bod
    
search_tag_in(['agile', 'estimation', 'iterative-development'])
