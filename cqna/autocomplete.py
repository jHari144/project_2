tag_list = ['Python', 'Java', 'C', 'C++', 'Ruby'] #add tags here
tag_result_list = []
id_list = ['Programmer1', 'Programmer2', 'Programmer3', 'Programmer4', 'Programmer5'] #add user IDs here
id_result_list = []
in_value = input("Enter search keyword: ")

temp = 0
for ele in tag_list:
    for i in range(len(in_value)):
        if len(in_value) <= len(ele):
            if in_value[i] == ele[i]:
                temp = temp + 1
    if temp == len(in_value):
        tag_result_list.append(ele)
    temp = 0
if len(tag_result_list) == 0:
    print('No tags found')
elif len(tag_result_list) == 1:
    print('1 tag found')   
else:
    print(len(tag_result_list), ' tag results found')
print(tag_result_list)
tag_result_list = []

id_result = 0
for ele in id_list:
    for i in range(len(in_value)):
        if len(in_value) <= len(ele):
            if in_value[i] == ele[i]:
                temp = temp + 1
    if temp == len(in_value):
        id_result_list.append(ele)
    temp = 0
if len(id_result_list) == 0:
    print('No IDs found')
elif len(id_result_list) == 1:
    print('1 ID found')   
else:
    print(len(id_result_list), ' ID results found')
print(id_result_list)
id_result_list = []
