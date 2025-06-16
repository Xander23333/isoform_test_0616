import pytest
import json
from controller import app
from model import User, Flag, Rule, Condition

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_flags_endpoint_normal(client):
    # 测试用例1：正常请求
    response = client.post('/flags', json={
        "name": "new_feature",
        "rules": [
            {
                "conditions": [
                    {"column": "region", "operator": "=", "value": "us"},
                    {"column": "tier", "operator": "=", "value": "pro"}
                ],
                "rollout": 100,
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

def test_flags_endpoint_empty(client):
    # 测试用例2：空请求
    response = client.post('/flags', json={})
    assert response.status_code == 400
    assert 'error' in response.data.decode()

def test_flags_endpoint_invalid_json(client):
    # 测试用例3：非JSON请求
    response = client.post('/flags', data='not json')
    assert response.status_code == 400
    assert 'error' in response.data.decode()

def test_evaluate_endpoint_normal(client):
    test_flags_endpoint_normal(client=client)
    response = client.post('/evaluate', json={
        "user_id": "user15",
        "flag": "new_feature"
    })
    print("Evaluate Response:", response.status_code, response.data.decode())  # 调试信息
    assert response.status_code == 200
    assert response.data.decode() == 'True'

def test_evaluate_endpoint_error(client):
    # 测试用例2：错误请求
    response = client.post('/evaluate', json={
        "user_id": "user14",
        "flag": "new_feature"
    })
    print("Evaluate Response:", response.status_code, response.data.decode())  # 调试信息
    assert response.status_code == 200
    assert response.data.decode() == 'False'

def test_evaluate_endpoint_empty(client):
    # 测试用例2：空请求
    response = client.post('/evaluate', json={})
    assert response.status_code == 400
    assert 'error' in response.data.decode()

def test_evaluate_endpoint_invalid_json(client):
    # 测试用例3：非JSON请求
    response = client.post('/evaluate', data='not json')
    assert response.status_code == 400
    assert 'error' in response.data.decode()

def test_user_data():
    assert len(test_users) == 20
    for user in test_users:
        assert user.user_id.startswith('user')
        assert user.region in ['us', 'eu', 'cn']
        assert user.tier in ['free', 'pro']

# 直接硬编码20个用户数据
test_users = [
    User(user_id='user0', region='us', tier='free'),
    User(user_id='user1', region='eu', tier='pro'),
    User(user_id='user2', region='cn', tier='free'),
    User(user_id='user3', region='us', tier='pro'),
    User(user_id='user4', region='eu', tier='free'),
    User(user_id='user5', region='cn', tier='pro'),
    User(user_id='user6', region='us', tier='free'),
    User(user_id='user7', region='eu', tier='pro'),
    User(user_id='user8', region='cn', tier='free'),
    User(user_id='user9', region='us', tier='pro'),
    User(user_id='user10', region='eu', tier='free'),
    User(user_id='user11', region='cn', tier='pro'),
    User(user_id='user12', region='us', tier='free'),
    User(user_id='user13', region='eu', tier='pro'),
    User(user_id='user14', region='cn', tier='free'),
    User(user_id='user15', region='us', tier='pro'),
    User(user_id='user16', region='eu', tier='free'),
    User(user_id='user17', region='cn', tier='pro'),
    User(user_id='user18', region='us', tier='free'),
    User(user_id='user19', region='eu', tier='pro')
]

if __name__ == "__main__":
    print("Running tests directly...")  # 调试信息
    client = app.test_client()  # 创建client实例
    test_flags_endpoint_normal(client)
    test_evaluate_endpoint_normal(client)