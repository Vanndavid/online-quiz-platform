
def averageScore(total_correct_answers, total_questions):
    #in percentage
    if total_questions == 0:
        return "0.00"
    average_score = (total_correct_answers / total_questions) * 100
    return "{:.2f}".format(average_score)


