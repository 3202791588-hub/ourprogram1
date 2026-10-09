import{request}from"./http";import{Result}from"../types/index"
export const getPreview=(id:number)=>request<Result>(`/results/${id}/preview`)
export const getFull=(id:number)=>request<Result>(`/results/${id}/full`)
export const unlock=(id:number)=>request(`/results/${id}/unlock`,"POST",{unlock_type:"MOCK"})
export const myResults=()=>request<Result[]>("/me/results")
