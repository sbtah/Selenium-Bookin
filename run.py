from bot.booking import MyBot


with MyBot(teardown=False) as bot:
    bot.land_first_page()
    bot.change_currency('PLN')
    bot.filter_destination('Połczyn-Zdrój')
    bot.pick_stay_date('2022-06-01', '2022-09-08')
    bot.send_adult_info(30)
    bot.send_children_info((10, 11, 17, 9))
    bot.pick_number_of_rooms(10)
    bot.send_all_info()