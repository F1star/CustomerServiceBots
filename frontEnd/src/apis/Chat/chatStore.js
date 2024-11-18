import { defineStore } from "pinia";
import { useTeleChatServer, useClearChatServer, useRepeatChatServer } from "./server";

export const useTeleChatStore = defineStore("teleChat",()=>{
    const server = useTeleChatServer();
    async function teleChat(data){
        const res = await server.teleChat(data);
        return res
    }
    const serverClear = useClearChatServer();
    async function clearChat(data) {
        const res = await serverClear.clearChat(data);
        return res
    }
    const serverRepeat = useRepeatChatServer();
    async function repeatChat(data) {
        const res = await serverRepeat.repeatChat(data);
        return res
    }
    return {
        teleChat,
        clearChat,
        repeatChat
    }
})