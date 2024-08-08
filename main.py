from classes.insta_bot import Bot



# ask the user if wants to shutdown the pc
# shudown = "y" == input("Do you want to shutdown the pc after the bot finishes? (y/n): ").lower().strip()
# time = int(input("Enter the time in in minutes to have the bot working: "))
bot = Bot()
bot.follow_random_users_from_page("happywinecol",2)
# bot.check_instagram(time * 60)


bot.bot_quit()
# if shudown: os.system("shutdown -h 0")