import random
from classes.insta_bot import Bot
import os

from helpers.txt_helpers import read_file_lines




print("Welcome to the Instagram Bot")
input("Press Enter to start the bot. . .")
os.system("clear")

target_pages = read_file_lines("TARGET_PAGES.txt")
amount_to_follow = int(input("How many users do you want to follow? "))

if input("By default the bot will watch randomly the instagram, for intervals of max, 5 minutes.\nDo you want to change this? (y/n): ").lower().strip() == "y":
  max_time_waching_instagram = int(input("How many minutes do you want the bot to watch instagram? "))
else:
  max_time_waching_instagram = 300
  

intervals_to_watch_instagram = [
  one_third:=max_time_waching_instagram / 3,
  one_third*2,
  one_third*3
]
print(f"The bot will watch instagram for max {max_time_waching_instagram/60} minutes, and will do it during random intervals of {" - ".join([str(i/60)for i in intervals_to_watch_instagram])} minutes.")

  
shudown = "y" == input("Do you want to shutdown the pc after the bot finishes? (y/n): ").lower().strip()

bot = Bot()
followed = 0
while followed < amount_to_follow:
  choosed_page = random.choice(target_pages)
  random_amount = random.randint(2, 6)
  print(f"Following {random_amount} users from {choosed_page}")
  bot.follow_random_users_from_page(choosed_page, random_amount)
  bot.check_instagram(random.choice(intervals_to_watch_instagram))


bot.bot_quit()
if shudown: os.system("shutdown -h 0")