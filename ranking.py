from operator import itemgetter

def averageScore(correct_answers, total_questions):
    
    return correct_answers / total_questions if total_questions > 0 else 0

def ranking(participants):
    for participant in participants:
        participant['score']=averageScore(participant['correct_answers'],participant['total_questions'])
    participants = sorted(participants, key=itemgetter('score'), reverse=True)
    n=1
    for participant in participants:
        participant['rank']=n
        n=n+1 
    return participants