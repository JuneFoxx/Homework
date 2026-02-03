from django.shortcuts import render, redirect
from .models import Poll, Question, Answer
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView


def index(request):
    polls = Poll.objects.all()
    poll_ids = [poll.id for poll in polls]

    some_dict = {}

    for poll in polls:
        some_dict[poll.title] = {}
        questions = Question.objects.filter(poll=poll.id)
        for question1 in questions:
            some_dict[poll.title].setdefault(question1.question, [])
            answers = Answer.objects.filter(question=question1.id)
            for answer in answers:
                some_dict[poll.title][question1.question].append(answer)

    return render(request, 'page/index.html', context= {
        "dict": some_dict,
        "poll_ids": poll_ids
    })

def create_poll(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        new_poll = Poll.objects.create(title=title)
        questions = request.POST.getlist('questions[]')
        question_ids = request.POST.getlist('question_ids[]')

        for q_index, question_text in enumerate(questions):
            question_id = question_ids[q_index]
            new_question = Question.objects.create(
                question=question_text,
                poll=new_poll
            )

            answers = request.POST.getlist(f'answers_{question_id}[]')
            for answer_text in answers:
                Answer.objects.create(
                    option=answer_text,
                    question=new_question
                )

    return redirect('page:index')


def get_poll_detailed(request, id: int): 
    poll = Poll.objects.get(id=id)
    some_dict = {}
    some_dict[poll.title] = {}
    questions = Question.objects.filter(poll=poll.id)
    for question1 in questions:
        some_dict[poll.title].setdefault(question1.question, [])
        answers = Answer.objects.filter(question=question1.id)
        for answer in answers:
            some_dict[poll.title][question1.question].append(answer)

    return render(request, 'page/index.html', context= {
        "dict": some_dict,
    })