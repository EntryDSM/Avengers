from typing import Any, Dict

from avengers.data.models.user import UserModel


def to_model(data: Dict[str, Any]) -> UserModel:
    return UserModel(
        email=data['email'],
        password=data['password'],
        receipt_code=data['receipt_code'],
        is_paid=data['is_paid'],
        is_printed_application_arrived=data['is_printed_application_arrived'],
        is_passed_first_apply=data['is_passed_first_apply'],
        is_passed_interview=data['is_passed_interview'],
        is_final_submit=data['is_final_submit'],
        exam_code=data['exam_code'],
        volunteer_score=data['volunteer_score'],
        attendance_score=data['attendance_score'],
        conversion_score=data['conversion_score'],
        final_score=data['final_score'],
    )


def to_raw() -> Dict[str, Any]:
    pass
