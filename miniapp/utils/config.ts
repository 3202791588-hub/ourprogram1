export const CLOUD_ENV_ID = "cloud1-d1gt8iwo343dfe428"
export const CLOUD_SERVICE_NAME = "personality-api"
export const API_PREFIX = "/api/v1"

// Keep the local HTTP endpoint available for local-only debugging. Real-device
// builds use CloudBase Run so that localhost never resolves to the phone.
export const USE_CLOUD_CONTAINER = true
export const LOCAL_API_BASE = "http://localhost/api/v1"
