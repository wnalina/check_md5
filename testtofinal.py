import cognitive_face as CF


SUBSCRIPTION_KEY = 'db816427ef814612975b8cb5479d3c8c'
BASE_URL = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)


# group_name = 'Test Group'
# group_id = 'testgroup'
# CF.person_group.create(group_id, group_name)

# group_id = 'testgroup'
# person_name = 'jame'
# person = CF.person.create(group_id, person_name)
# print(person)

# group_id = 'testgroup'
# person_name = 'jame'
# person_id = 'e972c5a2-db83-4d28-958e-b969fe362384'
# path = "D:/image/jame.jpg"
#
# CF.person.add_face(path, group_id, person_id)
# CF.person_group.train(group_id)
# response = CF.person_group.get_status(group_id)
# status = response['status']
# print('\t' + status)






img_path = 'D:/image/jame2.jpg'

azureDetect = CF.face.detect(img_path)

# print("\tazureDetect = " + str(azureDetect))





group_id = 'testgroup'
face_ids = [d['faceId'] for d in azureDetect]
azure_identified_faces = CF.face.identify(face_ids, group_id)
print("\tazureIdentify = " + str(azure_identified_faces))




# print('\t')
# print(azure_identified_faces)
# azureFound = len(face_ids)
#
# left = azureFound
# # print(azureFound)
# for count in range(azureFound):
#     candidate = azure_identified_faces[count]['candidates']
#     # print(candidate)
#     if not candidate:  # check empty list
#         print('\tname: unknown')
#         left -= 1
#     else:
#         candidate_personId = candidate[0]['personId']
#         candidate_confidence = candidate[0]['confidence']
#
#         for person in person_list:
#             if candidate_personId == person['personId']:
#                 print('\tname: ' + person['personName'] + ', with confidence: ' + str(candidate_confidence))
#                 left -= 1
#
# # print("left = " + str(left))
# for k in range(left):
#     print('\tname: ever known')
#
