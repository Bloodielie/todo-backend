from typing import List

from fastapi import APIRouter, HTTPException, Depends
from fastapidi import get_dependency
from fastapi.responses import ORJSONResponse

from app.modules.auth.depends import get_token_user
from app.modules.cards.dtos.card import Card, CreateCard, UpdateCard
from app.modules.cards.use_cases.interfaces import ICardService

router = APIRouter()


@router.get("/search", response_model=List[Card])
async def search_tasks(text: str, service=get_dependency(ICardService)):
    cards = await service.search_by_text(text)
    return ORJSONResponse([card.dict() for card in cards])


@router.get("/{id}", response_model=Card)
async def get(id: int, service=get_dependency(ICardService), user=Depends(get_token_user)):
    card = await service.get(id)
    if card is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if card.user_id != user.id:
        raise HTTPException(status_code=403, detail="Do not have permission to get this card")
    return ORJSONResponse(card.dict())


@router.get("/", response_model=List[Card])
async def get_all(service=get_dependency(ICardService), user=Depends(get_token_user)):
    cards = await service.get_by_user_id(user.id)
    return ORJSONResponse([card.dict() for card in cards])


@router.post("/", status_code=201, response_model=Card)
async def create(card: CreateCard, service=get_dependency(ICardService), user=Depends(get_token_user)):
    card = await service.create(card.text, user.id)
    if not card:
        raise HTTPException(status_code=400, detail="Failed to create record")
    return ORJSONResponse(card.dict(), status_code=201)


@router.delete("/{id}", response_model=Card)
async def delete(id: int, service=get_dependency(ICardService), user=Depends(get_token_user)):
    card = await service.get(id)
    if card is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if card.user_id != user.id:
        raise HTTPException(status_code=403, detail="Do not have permission to delete this card")

    card = await service.delete(id)
    if card is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ORJSONResponse(card.dict())


@router.patch("/{id}", response_model=Card)
async def update(
    id: int, update_card: UpdateCard, service=get_dependency(ICardService), user=Depends(get_token_user)
):
    card = await service.get(id)
    if card is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if card.user_id != user.id:
        raise HTTPException(status_code=403, detail="Do not have permission to update this card")

    update_card = await service.update(id, update_card)
    if update_card is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ORJSONResponse(update_card.dict())
