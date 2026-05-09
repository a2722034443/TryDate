"""
每周匹配定时任务（通过 Celery beat 在周日 20:00 触发）。
手动触发：python manage.py shell -> from matching.tasks import run_weekly_match; run_weekly_match()
"""
from django.utils import timezone
from django.db.models import Q
from users.models import User, BlackList
from questionnaire.models import Questionnaire
from .models import Match
from .algorithm import compute_compatibility, generate_highlights, gale_shapley


def get_week_number() -> str:
    return timezone.now().strftime('%Y-W%W')


def run_weekly_match():
    week = get_week_number()
    if Match.objects.filter(week_number=week).exists():
        print(f'[Match] Week {week} already matched.')
        return

    eligible = list(
        User.objects.filter(
            questionnaire_completion__gte=70,
            status=User.Status.ACTIVE,
            is_active=True,
        )
    )

    qs_map = {
        q.user_id: q.answers
        for q in Questionnaire.objects.filter(user__in=eligible)
    }

    blocked_pairs = set(
        BlackList.objects.values_list('blocker_id', 'blocked_id')
    )

    males = [u for u in eligible if u.gender == User.Gender.MALE
             and u.gender_preference in (User.GenderPreference.FEMALE, User.GenderPreference.BOTH)]
    females = [u for u in eligible if u.gender == User.Gender.FEMALE
               and u.gender_preference in (User.GenderPreference.MALE, User.GenderPreference.BOTH)]

    if not males or not females:
        print('[Match] Not enough users.')
        return

    scores = {}
    for m in males:
        for f in females:
            if (str(m.id), str(f.id)) in blocked_pairs or (str(f.id), str(m.id)) in blocked_pairs:
                continue
            a_ans = qs_map.get(m.id, {})
            b_ans = qs_map.get(f.id, {})
            score, _ = compute_compatibility(a_ans, b_ans)
            scores[(str(m.id), str(f.id))] = score
            scores[(str(f.id), str(m.id))] = score

    male_ids = [str(u.id) for u in males]
    female_ids = [str(u.id) for u in females]
    pairs = gale_shapley(male_ids, female_ids, scores)

    user_map = {str(u.id): u for u in eligible}
    created = 0
    for m_id, f_id in pairs.items():
        a_ans = qs_map.get(user_map[m_id].id, {})
        b_ans = qs_map.get(user_map[f_id].id, {})
        score, dim_scores = compute_compatibility(a_ans, b_ans)
        if score < 20:
            continue
        highlights = generate_highlights(a_ans, b_ans)
        Match.objects.create(
            user_a=user_map[m_id],
            user_b=user_map[f_id],
            compatibility_score=score,
            dimension_scores=dim_scores,
            compatibility_highlights=highlights,
            week_number=week,
        )
        created += 1

    print(f'[Match] Week {week}: created {created} matches.')
    return created
