from model import Flag, EvaluateRequest, Rule, Condition, User

# 模拟数据库
flags_map = {}
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

users = {user.user_id: user for user in test_users}

def parse_operator(operator, left, right):
    if operator == '=':
        return left == right
    elif operator == '!=':
        return left != right
    elif operator == '>':
        return left > right
    elif operator == '<':
        return left < right
    elif operator == '>=':
        return left >= right
    elif operator == '<=':
        return left <= right
    else:
        raise ValueError(f"Unsupported operator: {operator}")

def evaluate(user_id, flag_name):
    # 获取flag和user信息
    flag = flags_map.get(flag_name)
    if flag is None:
        return False
    user = users.get(user_id)
    if user is None:
        return False

    # 按优先级排序规则
    sorted_rules = sorted(flag.rules, key=lambda x: x.priority)
    
    # 遍历规则
    for rule in sorted_rules:
        # 检查rule所有condition是否满足

        conditions_met = True
        for condition in rule.conditions:
            # 获取用户对应字段的值
            user_value = getattr(user, condition.column)
            # 使用parse_operator检查条件
            if not parse_operator(condition.operator, user_value, condition.value):
                conditions_met = False
                break

        if conditions_met:
            # 如果有rollout设置
            if rule.rollout is not None:
                # 使用hash_value % 用户数量来算百分比
                import hashlib
                hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
                user_count = len(users)
                return (hash_value % user_count) < (rule.rollout * user_count / 100)
            # 如果没有rollout设置，直接返回True
            return True
    
    # 如果没有规则匹配，返回默认值
    return flag.default

def addOrUpdateFlag(flag):
    # 输入的flag是json，需要转换为Flag对象
    if isinstance(flag, dict):
        flag = Flag.from_dict(flag)
    elif isinstance(flag, Flag):
        pass
    else:
        raise TypeError("Expected dict or Flag object")
    flags_map[flag.name] = flag
    return True

if __name__ == "__main__":
    flags_map["new_feature"] = Flag(
        name="new_feature",
        rules=[
            Rule(
                conditions=[
                    Condition(column="region", operator="=", value="us"),
                    Condition(column="tier", operator="=", value="pro")
                ],
                priority=1
            )
        ],
        default=False
    )

    # 遍历user，测试new feature
    for user in test_users:
        print(user.user_id, evaluate(user.user_id, "new_feature"))