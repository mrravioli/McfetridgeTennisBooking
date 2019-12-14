import BookCourt, schedule, time
from datetime import datetime as dt

def action(daysInForward,startHour, emailAddress, password, cvv):
    success = BookCourt.BookCourt(daysInForward,startHour, emailAddress, password, cvv)
    print('BOOK SUCCESS: ', success)


if __name__ == '__main__':
    # start playing time
    startHour=3
    daysInForward=4

    emailAddress='**********'
    password='********'

    cvv='***'

    # # for instant booking
    # action(daysInForward,startHour,emailAddress,password,cvv)

    schedule.every().day.at("06:59").do(action,daysInForward,startHour,emailAddress,password,cvv)
    while 1:
        schedule.run_pending()
        time.sleep(1)
        # print(dt.now().strftime("%H:%M:%S"))s