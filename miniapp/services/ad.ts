import{unlock}from"./results"
export interface RewardedAdAdapter{unlockResult(resultId:number):Promise<void>}
export class MockRewardedAdAdapter implements RewardedAdAdapter{async unlockResult(resultId:number){await unlock(resultId)}}
// Production adapter should wrap wx.createRewardedVideoAd and call the AD verification endpoint only after onClose(isEnded=true).
export const rewardedAd:RewardedAdAdapter=new MockRewardedAdAdapter()
