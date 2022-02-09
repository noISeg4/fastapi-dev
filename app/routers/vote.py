from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models, database, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= "/vote",
    tags=["Vote"]
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def vote(vote_req: schemas.VoteBase, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    # check if the voted post exists
    post_query = db.query(models.Post).filter(models.Post.id == vote_req.post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id {vote_req.post_id} not found")

    # Get the vote
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote_req.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    # upvote or adding new vote
    if (vote_req.direction == 1):       
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT,
                                detail= f"user {current_user.id} already voted on post {vote_req.post_id}")

        new_vote = models.Vote(post_id= vote_req.post_id, user_id= current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    
    #downvote or delete preexisting vote
    else:
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                                detail= f"Vote does not exist")
        
        vote_query.delete(synchronize_session= False)
        db.commit()
        return {"message": "successfully deleted vote"}


