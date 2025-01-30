import pytest
from moto.dynamodb import 
from datetime import datetime
from pydantic import BaseModel, Field
from dynamodb_model import DynamoDBModel
import boto3

class TestUser(BaseModel):
    user_id: str = Field(alias="partition_key")
    email: str
    nickname: str = None
    created_at: datetime
    updated_at: datetime

@pytest.fixture
def dynamodb_table():
    with mock_dynamodb():
        # DynamoDB 리소스 생성
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
        
        # 테스트용 테이블 생성
        table = dynamodb.create_table(
            TableName='test-users',
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        yield table

@pytest.fixture
def user_model(dynamodb_table):
    return DynamoDBModel('test-users', TestUser)

def test_create_and_get_user(user_model):
    # Given
    now = datetime.now()
    new_user = TestUser(
        user_id="test123",
        email="test@example.com",
        nickname="tester",
        created_at=now,
        updated_at=now
    )
    
    # When
    user_model.put(new_user)
    retrieved_user = user_model.get("test123")
    
    # Then
    assert retrieved_user is not None
    assert retrieved_user.user_id == "test123"
    assert retrieved_user.email == "test@example.com"
    assert retrieved_user.nickname == "tester"

def test_update_user(user_model):
    # Given
    now = datetime.now()
    user = TestUser(
        user_id="test123",
        email="test@example.com",
        nickname="tester",
        created_at=now,
        updated_at=now
    )
    user_model.put(user)
    
    # When
    updated = user_model.update(
        partition_key="test123",
        update_data={
            "email": "updated@example.com",
            "nickname": "updated_tester"
        }
    )
    
    # Then
    assert updated.email == "updated@example.com"
    assert updated.nickname == "updated_tester"

def test_delete_user(user_model):
    # Given
    now = datetime.now()
    user = TestUser(
        user_id="test123",
        email="test@example.com",
        created_at=now,
        updated_at=now
    )
    user_model.put(user)
    
    # When
    user_model.delete("test123")
    
    # Then
    retrieved_user = user_model.get("test123")
    assert retrieved_user is None

def test_query_users(user_model):
    # Given
    now = datetime.now()
    users = [
        TestUser(
            user_id="test1",
            email="test1@example.com",
            nickname="tester1",
            created_at=now,
            updated_at=now
        ),
        TestUser(
            user_id="test2",
            email="test2@example.com",
            nickname="tester2",
            created_at=now,
            updated_at=now
        )
    ]
    
    for user in users:
        user_model.put(user)
    
    # When: Query with filter
    results = user_model.query(
        partition_key="test1",
        filter_expression={
            "email": {"operator": "begins_with", "value": "test1"}
        }
    )
    
    # Then
    assert len(results) == 1
    assert results[0].user_id == "test1"
    assert results[0].email == "test1@example.com"

def test_composite_key_model():
    # Given
    class CompositeUser(BaseModel):
        user_id: str = Field(alias="partition_key")
        email: str = Field(alias="sort_key")
        nickname: str
        created_at: datetime
    
    with mock_dynamodb():
        # Create table with composite key
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
        table = dynamodb.create_table(
            TableName='test-composite-users',
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                {'AttributeName': 'email', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        # Initialize model
        user_model = DynamoDBModel('test-composite-users', CompositeUser)
        
        # When
        now = datetime.now()
        user = CompositeUser(
            user_id="test123",
            email="test@example.com",
            nickname="tester",
            created_at=now
        )
        user_model.put(user)
        
        # Then: Get with composite key
        retrieved = user_model.get("test123", "test@example.com")
        assert retrieved is not None
        assert retrieved.user_id == "test123"
        assert retrieved.email == "test@example.com"
        
        # Query with sort key condition
        results = user_model.query(
            partition_key="test123",
            sort_key_condition={
                "operator": "begins_with",
                "value": "test"
            }
        )
        assert len(results) == 1

def test_invalid_key_access(user_model):
    # Then
    with pytest.raises(Exception):
        user_model.get("nonexistent-key")

def test_model_validation():
    # Given
    class ValidatedUser(BaseModel):
        user_id: str = Field(alias="partition_key")
        email: str
        age: int = Field(gt=0, lt=150)
    
    user_model = DynamoDBModel('test-users', ValidatedUser)
    
    # Then
    with pytest.raises(ValueError):
        ValidatedUser(
            user_id="test123",
            email="test@example.com",
            age=-1  # Invalid age
        )