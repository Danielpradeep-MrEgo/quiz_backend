import re
from bson import ObjectId

def generate_slug(title):
    """Generate a URL-friendly slug from a title"""
    # Convert to lowercase
    slug = title.lower()
    # Replace spaces and underscores with hyphens
    slug = re.sub(r'[\s_]+', '-', slug)
    # Remove all non-word characters except hyphens
    slug = re.sub(r'[^\w\-]', '', slug)
    # Replace multiple hyphens with single hyphen
    slug = re.sub(r'-+', '-', slug)
    # Remove leading and trailing hyphens
    slug = slug.strip('-')
    return slug

def generate_unique_slug(db, title, exclude_id=None):
    """Generate a unique slug by appending a number if needed"""
    base_slug = generate_slug(title)
    slug = base_slug
    counter = 1
    
    while True:
        query = {"slug": slug}
        if exclude_id:
            query["_id"] = {"$ne": ObjectId(exclude_id)}
        
        existing = db.quizzes.find_one(query)
        if not existing:
            return slug
        
        slug = f"{base_slug}-{counter}"
        counter += 1

