import random
from classes.insta_bot import Bot
import os

from helpers.txt_helpers import read_file_lines

default_target_pages_file = "TARGET_PAGES.txt"


os.system("clear")
os.system("cls")
print("Welcome to the Instagram Bot!")
print("*"*60)
  
# get the configuration from the user ------------------------------------------------


# get the action
print("\nSelect an action:")
print("1. Follow users")
print("2. Unfollow users")
action = ""
while action not in ["1", "2"]:
  action = input("Enter the number corresponding to your choice: ").strip()
  if action not in ["1", "2"]:
    print("Invalid input. Please enter '1' or '2'.")

while action not in ["1", "2"]:
  print("Invalid input. Please enter '1' or '2'.")
  action = input("Enter the number corresponding to your choice: ").strip()
action = "follow" if action == "1" else "unfollow"



max_time_waching_instagram_in_segs = 300  # default to 5 minutes
if input("\nBy default, the bot will watch Instagram for intervals of up to 5 minutes.\nDo you want to change this? (y/n): ").lower().strip() == "y":
  try:
    max_time_waching_instagram_in_segs = int(input("How many minutes do you want the bot to watch Instagram? ").strip()) * 60
  except ValueError:
    print("Invalid input. Using default value of 5 minutes.")
  

intervals_to_watch_instagram_in_segs = [
  one_third:=max_time_waching_instagram_in_segs / 3,
  one_third*2,
  one_third*3
]
print(f"\nThe bot will watch instagram for max {max_time_waching_instagram_in_segs/60} minutes, and will do it during random intervals of {" - ".join([str(round(i/60,1))for i in intervals_to_watch_instagram_in_segs])} minutes.")

shudown = "y" == input("Do you want to shutdown the pc after the bot finishes? (y/n): ").lower().strip()

# --------------------------------------------------------------------------------


if action == "unfollow":
  print("Unfollowing users is not implemented yet. Exiting.")
  # get the configuration --------------------------------------------
  amount_to_follow = int(input(f"How many users do you want to unfollow?: "))
  #-------------------------------------------------------------------
  bot = Bot()
  unfollowed = 0
  while unfollowed < amount_to_follow:
    amount_to_follow_now = random.randint(
      1,
      max( 10,((amount_to_follow-unfollowed ) - amount_to_follow//2))
    )
    print(f"\nUnfollowing {amount_to_follow_now} {amount_to_follow-unfollowed} left)users -----------")
    bot.unfollow_users(amount_to_follow_now)
    random_interval = random.choice(intervals_to_watch_instagram_in_segs)
    print("\n\n",f"Waching instagram for {random_interval/60} minutes. . .")
    bot.check_instagram(random_interval)
    unfollowed += amount_to_follow_now
elif action == "follow":
  print("Starting to follow users. . .")
  # get the configuration --------------------------------------------
  amount_to_follow = int(input(f"How many users do you want to follow?: "))
  # get file name
  file_name =  input("""Enter the name of the file containing target pages 
  (avoid the .txt extension, the bot will add it for you)
  (default is 'TARGET_PAGES.txt'): """).strip() 
  file_name = default_target_pages_file if not file_name else file_name
  target_pages = read_file_lines(file_name)
  #-------------------------------------------------------------------
  bot = Bot()
  followed = 0
  while followed < amount_to_follow:
    remaining_follows = amount_to_follow-followed
    print(f"{remaining_follows} missing to follow")
    choosed_page = random.choice(target_pages)
    random_amount = random.randint(3, 8) if remaining_follows > 8 else random.randint(1, remaining_follows)
    print(f"Following {random_amount} users from {choosed_page}")
    followed += bot.follow_random_users_from_page(choosed_page, random_amount)
    if followed >= amount_to_follow: break
    random_interval = max(60, random.choice(intervals_to_watch_instagram_in_segs))
    print("\n\n",f"Waching instagram for {random_interval/60} minutes. . .")
    bot.check_instagram(random_interval)



bot.bot_quit()
print(f"Bot finished following {amount_to_follow} users.")
if shudown:
  os.system("shutdown -h 0")
  # for windows
  os.system("shutdown /s /t 60")
