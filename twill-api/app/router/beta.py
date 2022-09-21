from fastapi import APIRouter, HTTPException, status
from twill.model.general import BannerResponse, BannerType
from twill.model.user import BetaAccess, BetaSignupRequest, BetaWaitlist

router = APIRouter()


@router.post("/signup")
async def verifier_login(req: BetaSignupRequest):
    # Check if already exists
    beta_access = await BetaAccess.find_one(BetaAccess.email == req.email)
    if beta_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You're already approved for beta access!",
        )

    beta_waitlist = await BetaWaitlist.find_one(BetaWaitlist.email == req.email)
    if beta_waitlist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You're already on the waitlist!",
        )

    # Create new beta waitlist
    beta_waitlist = BetaWaitlist(email=req.email)
    await beta_waitlist.insert()

    return {
        "banner": BannerResponse(
            message="You're added to the waitlist!", type=BannerType.success
        )
    }
