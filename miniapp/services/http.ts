import {
  API_PREFIX,
  CLOUD_ENV_ID,
  CLOUD_SERVICE_NAME,
  LOCAL_API_BASE,
  USE_CLOUD_CONTAINER,
} from "../utils/config"
import {getToken} from "../store/auth"

type HttpMethod = "GET" | "POST" | "PUT" | "DELETE"

export class ApiError extends Error {
  constructor(message: string, public status: number) {
    super(message)
  }
}

function headers(): Record<string, string> {
  return {
    Authorization: getToken() ? `Bearer ${getToken()}` : "",
    "Content-Type": "application/json",
    "X-WX-SERVICE": CLOUD_SERVICE_NAME,
  }
}

function unwrap<T>(statusCode: number, rawBody: unknown): T {
  const body = rawBody as any
  if (statusCode >= 200 && statusCode < 300) return body.data as T
  throw new ApiError(body?.message || "请求失败", statusCode)
}

function cloudRequest<T>(path: string, method: HttpMethod, data?: object): Promise<T> {
  return wx.cloud.callContainer({
    config: {env: CLOUD_ENV_ID},
    service: CLOUD_SERVICE_NAME,
    path: API_PREFIX + path,
    method,
    data,
    header: headers(),
  }).then(response => unwrap<T>(response.statusCode, response.data)).catch(error => {
    if (error instanceof ApiError) throw error
    throw new ApiError(error?.errMsg || "云托管服务暂不可用", 0)
  })
}

function localRequest<T>(path: string, method: HttpMethod, data?: object): Promise<T> {
  return new Promise((resolve, reject) => wx.request({
    url: LOCAL_API_BASE + path,
    method,
    data,
    header: headers(),
    success: response => {
      try {
        resolve(unwrap<T>(response.statusCode, response.data))
      } catch (error) {
        reject(error)
      }
    },
    fail: () => reject(new ApiError("网络不可用，请稍后重试", 0)),
  }))
}

export function request<T>(path: string, method: HttpMethod = "GET", data?: object): Promise<T> {
  return USE_CLOUD_CONTAINER
    ? cloudRequest<T>(path, method, data)
    : localRequest<T>(path, method, data)
}
