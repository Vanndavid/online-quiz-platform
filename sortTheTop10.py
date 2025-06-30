from operator import attrgetter
def sortTheTop10(quizzes):
    sorted_quizzes = sorted(quizzes, key=attrgetter('created_at'), reverse=True)
    return sorted_quizzes[:10]