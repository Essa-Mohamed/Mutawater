import json
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ScopeForm, TestTypeForm
from .models import TestSession, Question
from quran.services import QuranAPI
from quran.models import Ayah, Quarter, Hizb, Juz

def select_scope(request):
    if request.method == 'POST':
        form = ScopeForm(request.POST)
        if form.is_valid():
            # Save selections into session
            request.session['juzs'] = list(form.cleaned_data['juzs'].values_list('pk', flat=True))
            request.session['hizbs'] = list(form.cleaned_data['hizbs'].values_list('pk', flat=True))
            request.session['quarters'] = list(form.cleaned_data['quarters'].values_list('pk', flat=True))
            return redirect('exams:select_type')
    else:
        form = ScopeForm()

    # Load all quarters and their related Hizb → Juz chain
    quarters = Quarter.objects.all().select_related('hizb__juz')
    juz_to_quarters = {}
    hizb_to_quarters = {}

    for q in quarters:
        # via select_related we can reach q.hizb.juz_id
        juz_id = q.hizb.juz_id
        hizb_id = q.hizb_id

        juz_to_quarters.setdefault(juz_id, []).append(q.pk)
        hizb_to_quarters.setdefault(hizb_id, []).append(q.pk)

    return render(request, 'exams/select_scope.html', {
        'form': form,
        'juz_to_quarters_json': json.dumps(juz_to_quarters),
        'hizb_to_quarters_json': json.dumps(hizb_to_quarters),
    })


def select_type(request):
    if request.method == 'POST':
        form = TestTypeForm(request.POST)
        if form.is_valid():
            # Create a new test session
            session = TestSession.objects.create(
                student=request.user,
                test_type=form.cleaned_data['test_type'],
                num_questions=form.cleaned_data['num_questions'],
                difficulty=form.cleaned_data['difficulty'],
                score=0,
            )
            return redirect('exams:show_question', session_id=session.id, q_no=1)
    else:
        form = TestTypeForm()

    return render(request, 'exams/select_type.html', {'form': form})


def show_question(request, session_id, q_no):
    session = get_object_or_404(TestSession, id=session_id, student=request.user)
    if session.num_questions and q_no > session.num_questions:
        return redirect('exams:finish_test', session_id=session.id)

    # Pull the ayah IDs out of the session (should be set earlier)
    question_list = request.session.get('question_list', [])
    ayah = get_object_or_404(Ayah, id=question_list[q_no - 1])
    meta = QuranAPI.get_ayah(ayah.surah.number, ayah.number)

    # Build the list of available quarters based on the user's scope selection
    scope = {
        'juzs': request.session.get('juzs', []),
        'hizbs': request.session.get('hizbs', []),
        'quarters': request.session.get('quarters', []),
    }

    if scope['quarters']:
        quarter_ids = scope['quarters']
    elif scope['hizbs']:
        quarter_ids = Quarter.objects.filter(hizb_id__in=scope['hizbs']).values_list('id', flat=True)
    else:
        # only juzs selected → pull all quarters under those juzs via hizb→juz link
        quarter_ids = Quarter.objects.filter(hizb__juz_id__in=scope['juzs']).values_list('id', flat=True)

    quarters = Quarter.objects.filter(id__in=quarter_ids)
    pages = ayah.quarter.ayahs.values_list('page_number', flat=True).distinct()
    halves = [('TOP', 'أعلى'), ('BOTTOM', 'أسفل')]

    if request.method == 'POST':
        sel_q = int(request.POST['selected_quarter'])
        sel_p = int(request.POST['selected_page'])
        sel_h = request.POST['selected_half']

        correct = (
            meta['hizbQuarter'] == Quarter.objects.get(id=sel_q).number and
            meta['page'] == sel_p and
            meta.get('pageHalf', meta.get('page_half', 'TOP')) == sel_h
        )
        Question.objects.create(
            session=session,
            ayah=ayah,
            selected_quarter_id=sel_q,
            selected_page=sel_p,
            selected_half=sel_h,
            is_correct=correct
        )
        if correct:
            session.score += 1
            session.save()

        return redirect('exams:show_question', session_id=session.id, q_no=q_no + 1)

    return render(request, 'exams/question.html', {
        'session': session,
        'q_no': q_no,
        'verse_text': meta['text'],
        'quarters': quarters,
        'pages': pages,
        'halves': halves,
    })


def finish_test(request, session_id):
    session = get_object_or_404(TestSession, id=session_id, student=request.user)
    return render(request, 'exams/finish.html', {'session': session})
