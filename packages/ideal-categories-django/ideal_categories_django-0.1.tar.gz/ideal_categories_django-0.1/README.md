# Ideal Categories Django

This package provides a Django application for managing categories and subcategories using the Django REST framework.

## Installation

```bash
pip install ideal-categories-django
```
## Usage
Add `ideal_categories_django` to your `INSTALLED_APPS` in your Django settings.

```python
INSTALLED_APPS = [
    ...
    'ideal_categories_django',
    ...
]
```

Run migrations to create the necessary database tables:
```bash
python manage.py migrate
```

Endpoints

* `GET /categories/`: Fetch all categories in hierarchy.
* `GET /categories/{id}/`: Fetch category by ID.
* `POST /categories/`: Create a new category.
* `PUT /categories/{id}/`: Update an existing category.
* `DELETE /categories/{id}/`: Soft delete a category.

#### `LICENSE`
Choose an appropriate license for your project, such as MIT License. You can find license templates [here](https://choosealicense.com/).

#### `MANIFEST.in`
```plaintext
include README.md
include LICENSE
```