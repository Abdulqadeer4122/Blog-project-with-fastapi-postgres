from typing import List

from fastapi import APIRouter, status, HTTPException, Depends, Query, Path
from sqlalchemy import asc
from sqlalchemy.orm import Session, joinedload
from ..schemas.blog_schema import BlogContent, BlogResponse, AllBlogResponse
from ..Oath2 import get_current_user
from ..models.blog_model import Blog
from ..database import get_db
from ..models.user_model import User

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


@router.post("", response_description="Create Blog content", response_model=BlogResponse)
def create_blog(blog_content: BlogContent, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        blog_content_dict = blog_content.model_dump()
        blog_content_dict.update({"author_id": current_user.id, "author_name": current_user.username})
        new_blog = Blog(title=blog_content_dict["title"], body=blog_content_dict['body'],
                        author_id=blog_content_dict["author_id"])
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        blog_content_dict.update({"created_at": new_blog.created_at})
        blog_content_dict.update({"id": new_blog.id})
        return blog_content_dict
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.get('', response_description="get all blogs", response_model=List[BlogResponse])
def get_all_blog(limit: int = Query(4, ge=1), db: Session = Depends(get_db)):
    try:
        blogs = db.query(Blog).options(joinedload(Blog.author)).order_by(asc(Blog.created_at)).limit(limit).all()
        response = [
            BlogResponse(
                id=blog.id,
                title=blog.title,
                body=blog.body,
                created_at=blog.created_at,
                author_id=blog.author.id,
                author_name=blog.author.username
            )
            for blog in blogs
        ]
        return response
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.get('/{id}', response_description="get blog", response_model=BlogResponse)
def get_all_blog(id: str = Path(...), db: Session = Depends(get_db)):
    try:
        blog = db.query(Blog).options(joinedload(Blog.author)).filter(Blog.id == id).first()
        if blog is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The blog with this id doesn't exist!"
            )
        response = BlogResponse(
            id=blog.id,
            title=blog.title,
            body=blog.body,
            created_at=blog.created_at,
            author_id=blog.author.id,
            author_name=blog.author.username
        )
        return response
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.put('/{id}', response_description="update blog", response_model=BlogResponse)
def update_blog(id: str, blog_content: BlogContent, current_user=Depends(get_current_user),
                db: Session = Depends(get_db)):
    blog = db.query(Blog).options(joinedload(Blog.author)).filter(Blog.id == id).first()
    if current_user.id == blog.author.id:
        blog.title = blog_content.title
        blog.body = blog_content.body
        db.add(blog)
        db.commit()
        response = BlogResponse(
            id=blog.id,
            title=blog.title,
            body=blog.body,
            created_at=blog.created_at,
            author_id=blog.author.id,
            author_name=blog.author.username
        )
        return response

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not authorize to update this blog"
        )


@router.delete('/{id}', response_description="delete blog")
def delete_blog(id: str, current_user=Depends(get_current_user),
                db: Session = Depends(get_db)):
    blog = db.query(Blog).options(joinedload(Blog.author)).filter(Blog.id == id).first()
    if blog:
        if current_user.id == blog.author.id:
            db.delete(blog)
            db.commit()

            return {"Message": "Blog is delete successfully"}

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are not authorize to update this blog"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog with this id is not found "
        )
