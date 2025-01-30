from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from dynamodb_model import DynamoDBModel
from src.transaction_manager import TransactionScope

# Example Usage:
class UserModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )
    user_id: str = Field(alias='partition_key')
    email: str = Field(alias='sort_key')
    name: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

# Initialize the wrapper
user_db = DynamoDBModel[UserModel](
    table_name='test-users',
    model_class=UserModel
)

user_db2 = DynamoDBModel[UserModel](
    table_name='test-users2',
    model_class=UserModel
)

# Usage examples:
def example_usage():
    tx_scope = TransactionScope(user_db, user_db2)
    new_user1 = UserModel(
        user_id="user123",
        email="user@example.com",
        name="John Doe"
    )

    new_user2 = UserModel(
        user_id="user123",
        email="user@example.com",
        name="Trump"
    )
    with tx_scope.transaction():
        user_db.transact_put(new_user1)
        user_db2.transact_put(new_user2)

    # Create
    # print(new_user)
    # user_db.put(new_user)
    
    # Read
    # user = user_db.get("user123", "user@example.com")
    # print(user)
    # print(user)
    # Query
    # users = user_db.query(
    #     partition_key="user123",
    #     sort_key_condition={
    #         "operator": "begins_with",
    #         "value": "user"
    #     },
    #     filter_expression={
    #         "name": {
    #             "operator": "contains",
    #             "value": "John"
    #         }
    #     }
    # )
    # print(users)
    
    # # Update
    # updated_user = user_db.update(
    #     partition_key="user123",
    #     sort_key="user@example.com",
    #     update_data={
    #         "name": "John Smith",
    #         "updated_at": datetime.now()
    #     }
    # )
    # print(updated_user)
    # Delete
    # user_db.delete("user123", "user@example.com")

example_usage()