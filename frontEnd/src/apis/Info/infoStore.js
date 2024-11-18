import { defineStore } from "pinia";
import { useGetInfoServer, useSetInfoServer } from "./server";

export const useGetInfoStore = defineStore("getinfo",()=>{
    const server = useGetInfoServer();
    async function getInfo(data){
        const res = await server.getInfo(data);
        return res
    }
    return {
        getInfo
    }
})

export const useSetInfoStore = defineStore("setinfo",()=>{
    const server = useSetInfoServer();
    async function setInfo(data){
        const res = await server.setInfo(data);
        return res
    }
    return {
        setInfo
    }
})