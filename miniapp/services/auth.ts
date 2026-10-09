import{request}from"./http";import{setAuth}from"../store/auth"
export async function mockLogin(user:"user_a"|"user_b"){const d=await request<{access_token:string}>("/auth/wechat","POST",{mock_user:user});setAuth(d.access_token,user);return d}
