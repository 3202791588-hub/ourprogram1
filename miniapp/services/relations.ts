import{request}from"./http"
export const createInvite=(result_id:number)=>request<{invite_code:string;share_path:string}>("/relation-invites","POST",{result_id})
export const getInvite=(code:string)=>request<any>(`/relation-invites/${code}`)
export const acceptInvite=(code:string)=>request<{test_slug:string;invite_id:number}>(`/relation-invites/${code}/accept`,"POST")
export const getRelationship=(id:number)=>request<any>(`/relationships/${id}`)
export const myRelationships=()=>request<any[]>("/me/relationships")
