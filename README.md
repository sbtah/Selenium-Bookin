# Selenium Training Project

Whole idea of this mini project was to learn Selenium framework.
As a driver of test I chose a Firefox Geckodriver.


IMPORTANT! : On Ubuntu 22.04 Firefox is distributed as a snap package.
This actually caused an issue for me (Couldn't load profile). I had to remove snap and Install Firefox via APT.


Currently this BOT can:
-Request a Booking.com page,
-Change currency via implemented method : change_currency(),
-Filter destination with : filter_destination(),
-Pick date of booking from - to: pick_stay_date(),
-Pick number of adults: send_adult_info(),
-Pick number of childrens with their ages: send_children_info(),
-Pick number of rooms: pick_number_of_rooms().

