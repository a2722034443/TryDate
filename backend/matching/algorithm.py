"""
两阶段匹配算法：
  Phase 1 – 基于五维问卷计算任意两用户的契合度 (0-100)
  Phase 2 – Gale-Shapley 双向稳定匹配
"""
from __future__ import annotations
from typing import List, Dict, Tuple

WEIGHTS = {
    'basic': 0.15,
    'values': 0.40,
    'lifestyle': 0.25,
    'interests': 0.15,
    'date_pref': 0.05,
}

DIMENSION_KEYS = {
    'basic': [
        'grade', 'college_direction', 'target_grade_range',
        'height', 'target_height_range', 'relationship_status',
    ],
    'values': [
        'love_priorities', 'conflict_style', 'long_distance',
        'future_plan', 'love_role', 'space_need', 'money_attitude',
    ],
    'lifestyle': [
        'sleep_schedule', 'personality_type', 'ideal_weekend',
        'smoking_tolerance', 'food_style', 'exercise_habit', 'has_pet',
    ],
    'interests': ['hobbies', 'mbti', 'target_traits', 'self_description'],
    'date_pref': ['ideal_first_date', 'when_to_date'],
}


def _single_choice_score(a, b) -> float:
    if a is None or b is None:
        return 0.5
    if a == b:
        return 1.0
    try:
        diff = abs(int(a) - int(b))
    except (TypeError, ValueError):
        return 0.1
    if diff == 1:
        return 0.7
    if diff == 2:
        return 0.4
    return 0.1


def _scale_score(a, b, max_val=5) -> float:
    if a is None or b is None:
        return 0.5
    return 1.0 - abs(float(a) - float(b)) / (max_val - 1)


def _multi_choice_score(a: list, b: list) -> float:
    if not a or not b:
        return 0.0
    sa, sb = set(a), set(b)
    return len(sa & sb) / len(sa | sb)


def _range_score(val, target_range) -> float:
    if val is None or target_range is None:
        return 1.0
    if target_range == 'any':
        return 1.0
    try:
        lo, hi = target_range
        return 1.0 if lo <= val <= hi else 0.0
    except (TypeError, ValueError):
        return 0.5


def _calc_dimension_score(a_ans: dict, b_ans: dict, dim: str) -> float:
    keys = DIMENSION_KEYS[dim]
    scores = []
    for k in keys:
        av = a_ans.get(k)
        bv = b_ans.get(k)
        if k in ('love_priorities', 'hobbies', 'food_style', 'target_traits'):
            scores.append(_multi_choice_score(av or [], bv or []))
        elif k in ('long_distance', 'space_need', 'money_attitude'):
            scores.append(_scale_score(av, bv))
        elif k in ('target_height_range',):
            scores.append((_range_score(b_ans.get('height'), av) + _range_score(a_ans.get('height'), bv)) / 2)
        else:
            scores.append(_single_choice_score(av, bv))
    return sum(scores) / len(scores) if scores else 0.5


def compute_compatibility(a_ans: dict, b_ans: dict) -> Tuple[float, Dict[str, float]]:
    dim_scores = {dim: _calc_dimension_score(a_ans, b_ans, dim) for dim in WEIGHTS}
    total = sum(dim_scores[dim] * WEIGHTS[dim] for dim in WEIGHTS) * 100
    return round(total, 1), {k: round(v * 100, 1) for k, v in dim_scores.items()}


def generate_highlights(a_ans: dict, b_ans: dict) -> List[str]:
    highlights = []
    if a_ans.get('sleep_schedule') and a_ans.get('sleep_schedule') == b_ans.get('sleep_schedule'):
        label = '早鸟' if a_ans['sleep_schedule'] == 'early_bird' else '夜猫子'
        highlights.append(f'你们都是{label}，约好一起{("早餐" if label == "早鸟" else "夜宵")}吧～')
    a_hobbies = set(a_ans.get('hobbies') or [])
    b_hobbies = set(b_ans.get('hobbies') or [])
    common = a_hobbies & b_hobbies
    if common:
        hobby = list(common)[0]
        highlights.append(f'你们都喜欢{hobby}，聊起来一定有很多共同话题！')
    if a_ans.get('conflict_style') and a_ans.get('conflict_style') == b_ans.get('conflict_style'):
        highlights.append('你们处理争吵的方式很默契，沟通应该会比较顺畅！')
    if a_ans.get('future_plan') and a_ans.get('future_plan') == b_ans.get('future_plan'):
        highlights.append('你们对未来的方向很一致，走在同一条路上！')
    return highlights[:3]


def gale_shapley(
    proposers: List[str],
    receivers: List[str],
    scores: Dict[Tuple[str, str], float],
) -> Dict[str, str]:
    """
    经典 Gale-Shapley 算法（proposers 主动方）。
    返回 {proposer_id: receiver_id} 的稳定匹配对。
    """
    def pref(from_id, to_ids):
        return sorted(to_ids, key=lambda x: scores.get((from_id, x), 0), reverse=True)

    proposer_prefs = {p: pref(p, receivers) for p in proposers}
    receiver_prefs_rank = {
        r: {p: i for i, p in enumerate(pref(r, proposers))} for r in receivers
    }

    free_proposers = list(proposers)
    next_proposal = {p: 0 for p in proposers}
    receiver_held = {}

    while free_proposers:
        p = free_proposers.pop(0)
        if next_proposal[p] >= len(proposer_prefs[p]):
            continue
        r = proposer_prefs[p][next_proposal[p]]
        next_proposal[p] += 1

        if r not in receiver_held:
            receiver_held[r] = p
        else:
            current = receiver_held[r]
            rank = receiver_prefs_rank[r]
            if rank.get(p, 999) < rank.get(current, 999):
                receiver_held[r] = p
                free_proposers.append(current)
            else:
                free_proposers.append(p)

    return {p: r for r, p in receiver_held.items()}
