import tweepy

auth = tweepy.OAuth1UserHandler(
    consumer_key="tfQeSQmY5rg4m6tbue9KlwCl2",
    consumer_secret="6iaEmk0VxuX6OLsoJG5VIcV300qlOwHKuYTI9rwbntaoNa8NYI",
    access_token="106975972-y88v7fmzQL7vr77nmuvY2TpJJkRNlEN8PJvkPl1h",
    access_token_secret="eDKiJJJbOdHYVyjIZnw4XUmo6teTzJ1jK6kNLkQulAAhf"
)

api = tweepy.API(auth)
api.update_status("MadLads Says Hello!")
