from celery import Celery
import settings


app = Celery(settings.CELERY['name'],
             #backend='amqp://localhost:5672', #guest:guest@localhost:5672/', calhost:5672
             broker=settings.CELERY['broker'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)


if __name__ == '__main__':
    app.start()
