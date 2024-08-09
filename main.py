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
  max_time_waching_instagram_in_segs = int(input("How many minutes do you want the bot to watch instagram? "))*60
else:
  max_time_waching_instagram_in_segs = 300
  

intervals_to_watch_instagram_in_segs = [
  one_third:=max_time_waching_instagram_in_segs / 3,
  one_third*2,
  one_third*3
]
print(f"The bot will watch instagram for max {max_time_waching_instagram_in_segs/60} minutes, and will do it during random intervals of {" - ".join([str(i/60)for i in intervals_to_watch_instagram_in_segs])} minutes.")

  
shudown = "y" == input("Do you want to shutdown the pc after the bot finishes? (y/n): ").lower().strip()

bot = Bot()
followed = 0
while followed < amount_to_follow:
  choosed_page = random.choice(target_pages)
  random_amount = random.randint(3, 8) if amount_to_follow-followed > 8 else amount_to_follow-followed
  print(f"Following {random_amount} users from {choosed_page}")
  followed += bot.follow_random_users_from_page(choosed_page, random_amount)
  if followed >= amount_to_follow: break
  random_interval = random.choice(intervals_to_watch_instagram_in_segs)
  print("\n\n",f"Waching instagram for {random_interval/60} minutes. . .")
  bot.check_instagram(random_interval)


bot.bot_quit()
print(f"Bot finished following {amount_to_follow} users.")
if shudown: os.system("shutdown -h 0")
