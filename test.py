import cognitive_face as CF
import time


SUBSCRIPTION_KEY = 'db816427ef814612975b8cb5479d3c8c'
BASE_URL = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0'
PERSON_GROUP_ID = 'myfriends'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)

# CF.person_group.create(PERSON_GROUP_ID, 'My Friends')

# name = "Somsak2"
# user_data = 'More information can go here'
# response = CF.person.create(PERSON_GROUP_ID, name, user_data)
#
# # Get person_id from response
# person_id = response['personId']
# print(person_id)
#
# CF.person.add_face('https://i-h1.pinimg.com/564x/55/fa/21/55fa214a2f8f08d7c7587048f02ab17b.jpg', PERSON_GROUP_ID, person_id)

t = CF.person.lists(PERSON_GROUP_ID)
print(t)

person_groups = CF.person_group.lists()
print(person_groups)

print('Person Group List: '+str(len(person_groups)))
for person_group in person_groups:
    person_group_id = person_group['personGroupId']
    person_group_name = person_group['name']
    #CF.person_group.delete(person_group_id)
    print('\t{}'.format(person_group_id)+' NAME: {}'.format(person_group_name))
    # time.sleep(10)


# CF.person_group.train(PERSON_GROUP_ID)
#
# response = CF.person_group.get_status(PERSON_GROUP_ID)
# status = response['status']
# print(status)