from fastapi import APIRouter, HTTPException, status
from twill.model.general import Banner, BannerResponse, BannerType
from twill.model.user import BetaAccess, BetaSignupRequest, BetaWaitlist

router = APIRouter()


@router.post("/signup")
async def verifier_login(req: BetaSignupRequest):
    # Check if already exists
    beta_access = await BetaAccess.find_one(BetaAccess.email == req.email)
    if beta_access:
        return BannerResponse(
            banner=Banner(message="You already have access!", type=BannerType.info)
        )

    beta_waitlist = await BetaWaitlist.find_one(BetaWaitlist.email == req.email)
    if beta_waitlist:
        return BannerResponse(
            banner=Banner(
                message="You're already on the waitlist!", type=BannerType.info
            )
        )

    # Create new beta waitlist
    beta_waitlist = BetaWaitlist(email=req.email)
    await beta_waitlist.insert()

    return BannerResponse(
        banner=Banner(message="You're added to the waitlist!", type=BannerType.success)
    )
