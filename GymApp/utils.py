import random
import string

from GymApp.models import GymUser
from bullettinboard.models import Message


def create_users():
    GymUser.objects.all().delete()
    GymUser(username='admin', password='admin', ).save()
    GymUser(username='user1', password='user1', ).save()
    GymUser(username='user2', password='user2', ).save()
    GymUser(username='user3', password='user3', ).save()


def create_messages():
    Message.objects.all().delete()

    for _ in range(100):
        num_words = random.randint(100, 200)
        words = []
        for _ in range(num_words):
            word = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(1, 10)))
            words.append(word)
        sentence = ' '.join(words)
        Message(text=sentence, author=GymUser.objects.get(username='admin')).save()


