from .data import parent_categories

def up(cur):
    for parent_category in parent_categories.PARENT_CATEGORIES:
        cur.execute('''
            INSERT INTO parent_category_hierarchy (parent_category, category_order) 
            VALUES (%s, %s)
            ON CONFLICT (category_order) DO NOTHING
        ''', parent_category)
