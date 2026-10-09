const app=()=>getApp<{globalData:{token:string;mockUser:string}}>()
export const getToken=()=>app().globalData.token
export const getMockUser=()=>app().globalData.mockUser
export const setAuth=(token:string,user:string)=>{app().globalData.token=token;app().globalData.mockUser=user;wx.setStorageSync("token",token);wx.setStorageSync("mockUser",user)}
export const restoreAuth=()=>{app().globalData.token=wx.getStorageSync("token")||"";app().globalData.mockUser=wx.getStorageSync("mockUser")||"user_a"}
