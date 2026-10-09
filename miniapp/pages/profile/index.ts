import{request}from"../../services/http"
Page({data:{message:""},deleteData(){wx.showModal({title:"删除全部测试数据？",content:"此操作不可恢复。",success:async r=>{if(r.confirm){await request("/me/data","DELETE");wx.clearStorageSync();this.setData({message:"数据已删除"});wx.reLaunch({url:"/pages/home/index"})}}})}})
