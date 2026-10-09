import {CLOUD_ENV_ID, USE_CLOUD_CONTAINER} from "./utils/config"

App({
  onLaunch() {
    if (USE_CLOUD_CONTAINER) {
      wx.cloud.init({env: CLOUD_ENV_ID, traceUser: true})
    }
  },
  globalData: {token: "", mockUser: "user_a"},
})
