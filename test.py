import pytest
import json
from app import app
from data_define import User, Flag, Rule, Condition

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_flags_endpoint(client):
    # 测试用例1：正常请求
    response = client.post('/flags', json={
        "name": "new_feature",
        "rules": [
            {
                "conditions": [
                    {"column": "region", "operator": "=", "value": "us"},
                    {"column": "tier", "operator": "=", "value": "pro"}
                ],
                "rollout": 20,
                "priority": 1
            },
            {
                "conditions": [
                    {"column": "region", "operator": "!=", "value": "cn"}
                ],
                "priority": 2
            }
        ],
        "default": False
    })
    assert response.status_code == 200
    assert response.data.decode() == 'True'

    # 测试用例2：空请求
    response = client.post('/flags', json={})
    assert response.status_code == 400
    assert response.data.decode() == 'False'

    # 测试用例3：非JSON请求
    response = client.post('/flags', data='not json')
    assert response.status_code == 400
    assert response.data.decode() == 'False'

def test_evaluate_endpoint(client):
    response1 = client.post('/flags', json={
        "name": "new_feature",
        "rules": [
            {
                "conditions": [
                    {"column": "region", "operator": "=", "value": "us"},
                    {"column": "tier", "operator": "=", "value": "pro"}
                ],
                "priority": 1
            }
        ],
        "default": False
    })
    print("Flags Response:", response1.status_code, response1.data.decode())  # 调试信息

    # 测试用例1：正常请求
    response = client.post('/evaluate', json={
        "user_id": "user15",
        "flag": "new_feature"
    })
    print("Evaluate Response:", response.status_code, response.data.decode())  # 调试信息
    assert response.status_code == 200
    assert response.data.decode() == 'True'

    # 测试用例2：错误请求
    response = client.post('/evaluate', json={
        "user_id": "user14",
        "flag": "new_feature"
    })
    print("Evaluate Response:", response.status_code, response.data.decode())  # 调试信息
    assert response.status_code == 200
    assert response.data.decode() == 'False'

    # 测试用例2：空请求
    response = client.post('/evaluate', json={})
    assert response.status_code == 400
    assert response.data.decode() == 'False'

    # 测试用例3：非JSON请求
    response = client.post('/evaluate', data='not json')
    assert response.status_code == 400
    assert response.data.decode() == 'False'

def test_user_data():
    assert len(test_users) == 20
    for user in test_users:
        assert user.user_id.startswith('user')
        assert user.region in ['us', 'eu', 'cn']
        assert user.tier in ['free', 'pro']

if __name__ == "__main__":
    print("Running tests directly...")  # 调试信息
    client = app.test_client()  # 创建client实例
    test_evaluate_endpoint(client)