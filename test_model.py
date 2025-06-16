import pytest
from model import Condition, Rule, Flag, EvaluateRequest, User

def test_condition_serialization():
    condition = Condition(column="region", operator="=", value="us")
    condition_dict = condition.dict()
    assert condition_dict == {"column": "region", "operator": "=", "value": "us"}
    condition_from_dict = Condition(**condition_dict)
    assert condition_from_dict == condition

def test_rule_serialization():
    condition = Condition(column="region", operator="=", value="us")
    rule = Rule(conditions=[condition], priority=1, rollout=20)
    rule_dict = rule.dict()
    assert rule_dict == {"conditions": [{"column": "region", "operator": "=", "value": "us"}], "priority": 1, "rollout": 20}
    rule_from_dict = Rule(**rule_dict)
    assert rule_from_dict == rule

def test_flag_serialization():
    condition = Condition(column="region", operator="=", value="us")
    rule = Rule(conditions=[condition], priority=1, rollout=20)
    flag = Flag(name="new_feature", rules=[rule], default=False)
    flag_dict = flag.dict()
    assert flag_dict == {"name": "new_feature", "rules": [{"conditions": [{"column": "region", "operator": "=", "value": "us"}], "priority": 1, "rollout": 20}], "default": False}
    flag_from_dict = Flag(**flag_dict)
    assert flag_from_dict == flag

def test_evaluate_request_serialization():
    evaluate_request = EvaluateRequest(user_id="user15", flag="new_feature")
    evaluate_request_dict = evaluate_request.dict()
    assert evaluate_request_dict == {"user_id": "user15", "flag": "new_feature"}
    evaluate_request_from_dict = EvaluateRequest(**evaluate_request_dict)
    assert evaluate_request_from_dict == evaluate_request

def test_user_serialization():
    user = User(user_id="user15", region="us", tier="pro")
    user_dict = user.dict()
    assert user_dict == {"user_id": "user15", "region": "us", "tier": "pro"}
    user_from_dict = User(**user_dict)
    assert user_from_dict == user 