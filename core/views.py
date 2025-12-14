# core/views.py

from django.shortcuts import render, get_object_or_404
from .models import User, BookEdition, Grade, Topic, PracticeQuestion,TestQuestion,Test,Announcement
from django.shortcuts import redirect

def home(request):
    tg_id = request.GET.get("id")
    user = get_object_or_404(User, tg_id=tg_id)

    # Faqat faol (is_active=True) bo'lgan birinchi bildirishnomani olish
    announcement = Announcement.objects.filter(is_active=True).first()

    return render(request, "index.html", {
        "name": user.name,
        "tg_id": tg_id,
        "balance": user.balance,
        "is_premium": user.is_premium,
        "announcement": announcement,  # ✅ yangi kontekst
    })

# 1. Darslik davrlari
def select_edition(request):
    tg_id = request.GET.get("id")
    user = get_object_or_404(User, tg_id=tg_id)
    editions = BookEdition.objects.all()
    return render(request, "select_edition.html", {
        "editions": editions,
        "tg_id": tg_id
    })

# 2. Sinf tanlash
def select_grade(request, edition_id):
    tg_id = request.GET.get("id")
    user = get_object_or_404(User, tg_id=tg_id)
    edition = get_object_or_404(BookEdition, id=edition_id)
    grades = Grade.objects.all()
    return render(request, "select_grade.html", {
        "edition": edition,
        "grades": grades,
        "tg_id": tg_id
    })

# 3. Mavzu tanlash
def select_topic(request, edition_id, grade_id):
    tg_id = request.GET.get("id")
    user = get_object_or_404(User, tg_id=tg_id)
    edition = get_object_or_404(BookEdition, id=edition_id)
    grade = get_object_or_404(Grade, id=grade_id)
    topics = Topic.objects.filter(edition=edition, grade=grade)
    return render(request, "select_topic.html", {
        "edition": edition,
        "grade": grade,
        "topics": topics,
        "tg_id": tg_id
    })

# 4. Savollar ko'rsatish
def show_questions(request, topic_id):
    tg_id = request.GET.get("id")
    user = get_object_or_404(User, tg_id=tg_id)
    topic = get_object_or_404(Topic, id=topic_id)
    questions = topic.questions.all()
    return render(request, "show_questions.html", {
        "topic": topic,
        "questions": questions,
        "tg_id": tg_id
    })


# 1. Testlar → Davrlar
def test_select_edition(request):
    tg_id = request.GET.get("id")
    user = get_object_or_404(User, tg_id=tg_id)
    if not user.is_premium:
        return render(request, "error.html", {"error": "Premium kerak", "tg_id": tg_id})
    editions = BookEdition.objects.all()
    return render(request, "test_select_edition.html", {"editions": editions, "tg_id": tg_id})

# 2. Sinf tanlash
def test_select_grade(request, edition_id):
    tg_id = request.GET.get("id")
    user = get_object_or_404(User, tg_id=tg_id)
    if not user.is_premium:
        return redirect(f"/?id={tg_id}")
    edition = get_object_or_404(BookEdition, id=edition_id)
    grades = Grade.objects.all()
    return render(request, "test_select_grade.html", {
        "edition": edition,
        "grades": grades,
        "tg_id": tg_id
    })

# 3. Mavzu tanlash
def test_select_topic(request, edition_id, grade_id):
    tg_id = request.GET.get("id")
    user = get_object_or_404(User, tg_id=tg_id)
    if not user.is_premium:
        return redirect(f"/?id={tg_id}")
    edition = get_object_or_404(BookEdition, id=edition_id)
    grade = get_object_or_404(Grade, id=grade_id)
    topics = Topic.objects.filter(edition=edition, grade=grade)
    return render(request, "test_select_topic.html", {
        "edition": edition,
        "grade": grade,
        "topics": topics,
        "tg_id": tg_id
    })

# 4. Testni yechish
# core/views.py

def test_questions(request, topic_id):
    tg_id = request.GET.get("id")
    user = get_object_or_404(User, tg_id=tg_id)
    if not user.is_premium:
        return redirect(f"/?id={tg_id}")
    
    topic = get_object_or_404(Topic, id=topic_id)
    # ✅ TO'G'RI: TestQuestion → test → topic
    questions = TestQuestion.objects.filter(test__topic=topic)

    if request.method == "POST":
        total = questions.count()
        correct = 0
        results = []

        for q in questions:
            selected = request.POST.get(f"q{q.id}", "").strip()
            is_correct = (selected == q.correct_answer)
            if is_correct:
                correct += 1

            results.append({
                'question': q,
                'selected': selected,
                'is_correct': is_correct,
                'correct_answer': q.correct_answer,
            })

        percentage = round((correct / total) * 100, 1) if total > 0 else 0

        return render(request, "test_result.html", {
            "correct": correct,
            "total": total,
            "percentage": percentage,
            "topic": topic,
            "tg_id": tg_id,
            "results": results,
        })

    return render(request, "test_questions.html", {
        "topic": topic,
        "questions": questions,
        "tg_id": tg_id
    })

def top_up_balance(request):
    tg_id = request.GET.get('id')
    user = get_object_or_404(User, tg_id=tg_id)
    return render(request, 'top_up_balance.html', {
        'user': user,
        'tg_id': tg_id
    })




# views.py
from django.shortcuts import render
from .models import PaymentSettings

def top_up_balance(request):
    tg_id = request.GET.get('id')
    user = None
    if tg_id and tg_id.isdigit():
        user = get_object_or_404(User, tg_id=int(tg_id))
    else:
        # ID noto'g'ri bo'lsa, anonim foydalanuvchi sifatida davom ettirish ham mumkin
        user = type('obj', (object,), {'full_name': 'Mehmon foydalanuvchi'})

    settings = PaymentSettings.objects.first()
    if not settings:
        settings = PaymentSettings.objects.create()

    return render(request, 'top_up_balance.html', {
        'user': user,
        'tg_id': tg_id,
        'settings': settings,
    })