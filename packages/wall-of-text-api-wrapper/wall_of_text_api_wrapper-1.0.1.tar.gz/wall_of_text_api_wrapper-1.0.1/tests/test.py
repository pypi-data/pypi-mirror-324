from src.wall_of_text_api_wrapper import WallOfTextAPIWrapperLatest

# api_server = "http://127.0.0.1:8001/apis/wall_of_text"
api_server = "https://pashok11.tw1.su/apis/wall_of_text"
api = WallOfTextAPIWrapperLatest(api_server)

for t in api.get_texts():
    print(t)

# get_one_text = api.get_text(6, False)
# print("\n====> get_one_text:\n", get_one_text)

# get_comments = api.get_texts(parent_id=6, include_comments=False)
# print("\n====> get_comments:\n")
# for c in get_comments:
#     print(c)


# create_text = api.create_text(
#     text="Hello, updated API!",
#     username="Pashok11",
#     parent_id=1
# )
# print("\n====> create_text:\n", create_text)
