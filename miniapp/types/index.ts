export interface Option{id:number;label:string;content:string;sequence:number}
export interface QuestionMetadata{title?:string;scene_key?:string;scene_asset?:string;chapter?:string;motion_preset?:string;layout?:string}
export interface Question{id:number;sequence:number;type:string;content:string;metadata?:QuestionMetadata;options:Option[]}
export interface TestDetail{slug:string;name:string;description:string;current_version:{id:number;version:number;question_count:number;questions:Question[]}}
export interface Session{id:number;status:string;current_question:number;relation_invite_id?:number;questions?:Question[];answers:{question_id:number;option_id:number}[]}
export interface Result{id:number;result_type:string;name:string;tags:string[];summary:string;dimension_scores:Record<string,number>;is_unlocked:boolean;sections?:{title:string;content:string}[]}
