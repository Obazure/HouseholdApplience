""" TEST module contains set of tests to check endpoints
and passing and responding data formats
"""
import pytest
from starlette.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.skip
def test_entity_content(post_content, fake_data_set=None):
    """Helper to test pizza structure

    :param post_content: structure of pizza to test
    :param fake_data_set: set to be compared with
    """
    assert post_content['id']
    assert post_content['id'] > 0
    assert post_content['status']
    assert post_content['status'] in ['waiting', 'ready']
    assert 'ingredients' in post_content
    assert isinstance(post_content['ingredients'], list)
    if len(post_content['ingredients']) > 0:
        for idx, ingredient in enumerate(post_content['ingredients']):
            assert ingredient and ingredient['id'] > 0
            if fake_data_set:
                assert ingredient['name'] == str(
                    fake_data_set['ingredients'][idx]['name'])
                assert ingredient['count'] == int(
                    fake_data_set['ingredients'][idx]['count'])
            else:
                assert isinstance(ingredient['name'], str)
                assert isinstance(ingredient['count'], int)


fake_data = {
    "name": "margarita",
    "ingredients": [
        {
            "name": "cheese",
            "count": 1,
        },
        {
            "name": "tomato",
            "count": 2,
        }
    ],
    "status": "waiting",
}


def test_post_pizza():
    """ Test post endpoint and response format checking
    """
    post_response = client.post("/api/pizzas/", json=fake_data)
    assert post_response.status_code == 200
    post_content = post_response.json()
    test_entity_content(post_content, fake_data)


fake_data_for_ingredients_array_error = {
    "name": "vegetarien",
    "ingredients": ["cheese"],
    "status": "waiting"
}

error_msg_for_ingredient_array = {
    "detail": [
        {
            "loc": [
                "body",
                "ingredients",
                0
            ],
            "msg": "value is not a valid dict",
            "type": "type_error.dict"
        }
    ]
}


def test_wrong_ingredients_format():
    """ Test post endpoint with wrong format when Ingredient passed as array
    """
    post_response = client.post("/api/pizzas/",
                                json=fake_data_for_ingredients_array_error)
    assert post_response.status_code == 422
    assert post_response.json() == error_msg_for_ingredient_array


fake_data_for_ingredients_with_wrong_count = {
    "name": "vegetarien",
    "ingredients": [
        {
            "name": "cheese",
            "count": "asdf",
        }
    ],
    "status": "waiting"
}

error_msg_for_ingredients_with_wrong_count = {
    "detail": [
        {
            "loc": [
                "body",
                "ingredients",
                0,
                "count"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}


def test_wrong_ingredient_count_format_string():
    """ Test post endpoint with wrong Ingredient str as str count field sent
    """
    post_response = client.post(
        "/api/pizzas/",
        json=fake_data_for_ingredients_with_wrong_count
    )
    assert post_response.status_code == 422
    assert post_response.json() == error_msg_for_ingredients_with_wrong_count


fake_data_for_ingredient_count_format_string_number = {
    "name": "vegetarien",
    "ingredients": [
        {
            "name": "cheese",
            "count": "111",
        }
    ],
    "status": "waiting"
}


def test_wrong_ingredient_count_format_number_in_string():
    """ Test post endpoint with wrong Ingredient num as str count field sent
       """
    post_response = client.post(
        "/api/pizzas/",
        json=fake_data_for_ingredient_count_format_string_number
    )
    assert post_response.status_code == 200
    post_content = post_response.json()
    test_entity_content(post_content,
                        fake_data_for_ingredient_count_format_string_number)


fake_data_with_impressive_id = {
    "id": 9999,
    "name": "Extraordinary pizza",
    "ingredients": [],
    "status": "waiting"
}


def test_put_pizza_with_wrong_id():
    """ Test put endpoint when non existing pizza id passed
    """
    response = client.put("/api/pizzas/", json=fake_data_with_impressive_id)
    assert response.status_code == 404
    content = response.json()
    assert content['detail'] == "Item not found or value is incorrect."


def test_get_pizza_list():
    """ Test get endpoint with list structure checking
    """
    response = client.get("/api/pizzas/")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) > 0
    for entity in content:
        test_entity_content(entity)
