from classes.insta_bot import Bot
import os



# ask the user if wants to shutdown the pc
shudown = "y" == input("Do you want to shutdown the pc after the bot finishes? (y/n): ").lower().strip()
time = int(input("Enter the time in in minutes to have the bot working: "))
bot = Bot()
bot.check_instagram(time * 60)
bot.bot_quit()
if shudown:
    print("Shutting down the pc ")
    os.system("shutdown -h 0")