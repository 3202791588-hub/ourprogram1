import{request}from"./http";import{Session,TestDetail}from"../types/index"
export const getTest=(slug="hidden-personality")=>request<TestDetail>(`/tests/${slug}`)
export const createSession=(test_slug="hidden-personality",relation_invite_id?:number)=>request<Session>("/test-sessions","POST",{test_slug,...(relation_invite_id?{relation_invite_id}:{})})
export const getSession=(id:number)=>request<Session>(`/test-sessions/${id}`)
export const saveAnswer=(id:number,question_id:number,option_id:number)=>request(`/test-sessions/${id}/answers`,"PUT",{question_id,option_id})
export const submitSession=(id:number)=>request<{result_id:number;relationship_id?:number}>(`/test-sessions/${id}/submit`,"POST")
