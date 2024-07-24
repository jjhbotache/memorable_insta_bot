from helpers.insta_helpers import get_data_from_insta_user
from helpers.data_parser import user_data_to_potential_buyer


user = input("Enter a username to analyse: ")
user_data = get_data_from_insta_user(user)
user_data_to_potential_buyer(user_data)



