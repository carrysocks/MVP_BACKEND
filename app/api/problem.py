from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter()

# 미리 생성된 S3 링크를 저장하는 딕셔너리
image_links = {
    "earth_science": {
        1: [
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/earth_science/level1/earth1_1.png",
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/earth_science/level1/earth1_2.png",
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/earth_science/level1/earth1_3.png",
        ],
        2: [
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/earth_science/level1/earth2_1.png",
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/earth_science/level1/earth2_2.png",
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/earth_science/level1/earth2_3.png",
        ],
        3: [
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/earth_science/level1/earth3_1.png",
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/earth_science/level1/earth3_2.png",
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/earth_science/level1/earth3_3.png",
        ]
    },
    "life_science": {
        1: [
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/life_science/level1/life1_1.png",
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/life_science/level1/life1_2.png",
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/life_science/level1/life1_3.png",
        ],
        2: [
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/life_science/level1/life2_1.png",
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/life_science/level1/life2_2.png",
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/life_science/level1/life2_3.png",
        ],
        3: [
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/life_science/level1/life3_1.png",
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/life_science/level1/life3_2.png",
            "https://aisip-mvp-science-problems.s3.ap-northeast-2.amazonaws.com/life_science/level1/life3_3.png",
        ]
    },
}


class FeedbackRequest(BaseModel):
    selections: List[bool]


class FeedbackResponse(BaseModel):
    feedback: str
    score: int
    percentage: float
    grade: int
    score_diff: int
    percentage_diff: float
    grade_diff: int


def calculate_feedback_and_score(problem_id: int, selections: List[str]):
    problem_data = {
        0: {"answer": [True, True, True], "accuracy": 0, "score": 0, "cumulative_score": 0, "percentage": 0,
            "grade": 9},
        1: {"answer": [False, True, False], "accuracy": 92, "score": 142, "cumulative_score": 142, "percentage": 21,
            "grade": 6},
        2: {"answer": [True, True, True], "accuracy": 96, "score": 92, "cumulative_score": 234, "percentage": 33,
            "grade": 6},
        3: {"answer": [True, True, False], "accuracy": 91, "score": 158, "cumulative_score": 392, "percentage": 57,
            "grade": 5},
        4: {"answer": [True, True, True], "accuracy": 81, "score": 258, "cumulative_score": 650, "percentage": 63,
            "grade": 4},
        5: {"answer": [True, False, False], "accuracy": 78, "score": 292, "cumulative_score": 942, "percentage": 76,
            "grade": 3},
        6: {"answer": [False, False, True], "accuracy": 75, "score": 325, "cumulative_score": 1267, "percentage": 82,
            "grade": 3},
        7: {"answer": [False, False, True], "accuracy": 73, "score": 358, "cumulative_score": 1625, "percentage": 90,
            "grade": 2},
        8: {"answer": [True, True, False], "accuracy": 55, "score": 525, "cumulative_score": 2150, "percentage": 95,
            "grade": 2},
        9: {"answer": [False, True, False], "accuracy": 50, "score": 600, "cumulative_score": 2750, "percentage": 97,
            "grade": 1},
        10: {"answer": [True, True, True], "accuracy": 0, "score": 0, "cumulative_score": 0, "percentage": 0,
             "grade": 9},
        11: {"answer": [True, False, True], "accuracy": 93, "score": 130, "cumulative_score": 130, "percentage": 22,
             "grade": 6},
        12: {"answer": [True, False, True], "accuracy": 91, "score": 145, "cumulative_score": 275, "percentage": 40,
             "grade": 5},
        13: {"answer": [True, True, False], "accuracy": 88, "score": 170, "cumulative_score": 445, "percentage": 61,
             "grade": 4},
        14: {"answer": [True, False, True], "accuracy": 89, "score": 250, "cumulative_score": 695, "percentage": 68,
             "grade": 4},
        15: {"answer": [True, False, False], "accuracy": 73, "score": 305, "cumulative_score": 1000, "percentage": 78,
             "grade": 3},
        16: {"answer": [True, False, False], "accuracy": 71, "score": 335, "cumulative_score": 1335, "percentage": 88,
             "grade": 2},
        17: {"answer": [False, True, True], "accuracy": 67, "score": 365, "cumulative_score": 1700, "percentage": 92,
             "grade": 2},
        18: {"answer": [True, True, False], "accuracy": 68, "score": 530, "cumulative_score": 2230, "percentage": 96,
             "grade": 1},
        19: {"answer": [False, True, False], "accuracy": 48, "score": 610, "cumulative_score": 2840, "percentage": 98,
             "grade": 1},
    }

    is_correct = selections == problem_data[problem_id]["answer"]

    if is_correct:
        feedback = "정답입니다! 잘하셨어요."
    else:
        feedback = "아쉽게도 틀렸습니다."

    accuracy = problem_data[problem_id]["accuracy"]
    if accuracy >= 90:
        feedback += " 대부분의 학생들도 맞힌 문제예요!"
    elif accuracy >= 70:
        feedback += " 많은 학생들이 맞히기 어려워하는 문제입니다."
    else:
        feedback += " 상위권 학생들도 어려워하는 고난도 문제예요. 잘 해결하셨습니다!"

    score = problem_data[problem_id]["cumulative_score"] if is_correct else 0
    score_diff = problem_data[problem_id]["score"] if is_correct else 0
    percentage = problem_data[problem_id]["percentage"] if is_correct else 0
    grade = problem_data[problem_id]["grade"] if is_correct else 0

    prev_problem_id = problem_id - 1
    prev_percentage = problem_data.get(prev_problem_id, {}).get("percentage", 0)
    prev_grade = problem_data.get(prev_problem_id, {}).get("grade", 0)

    percentage_diff = percentage - prev_percentage
    grade_diff = prev_grade - grade

    return {
        "feedback": feedback,
        "score": score,
        "percentage": percentage,
        "grade": grade,
        "score_diff": score_diff,
        "percentage_diff": percentage_diff,
        "grade_diff": grade_diff,
    }


@router.get("/problems/earth_science", response_model=dict)
def get_earth_science_problems():
    return image_links["earth_science"]


@router.get("/problems/life_science", response_model=dict)
def get_life_science_problems():
    return image_links["life_science"]


@router.post("/problems/{problem_id}/feedback", response_model=FeedbackResponse)
def get_problem_feedback(problem_id: int, request: FeedbackRequest):
    if problem_id < 1 or problem_id > 19 or problem_id == 10:
        raise HTTPException(status_code=404, detail="Problem not found")

    feedback_response = calculate_feedback_and_score(problem_id, request.selections)
    return feedback_response

