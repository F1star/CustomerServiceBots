import { defineStore } from "pinia";
import { SERVER_CONFIG } from "../../config";
import axios from "axios";

export const useTeleChatServer = defineStore("TeleChatServer", () => {
    const server = axios.create({
        baseURL: SERVER_CONFIG.SERVER + ":" + SERVER_CONFIG.PORT,
        timeout: 20000,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
    })
    const teleChat = async (data) => {
        const res = await server.post("telechat", data)
        return res
    }
    return {
        teleChat
    }
})

export const useClearChatServer = defineStore("ClearChatServer", () => {
    const server = axios.create({
        baseURL: SERVER_CONFIG.SERVER + ":" + SERVER_CONFIG.PORT,
        timeout: 20000,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
    })
    const clearChat = async (data) => {
        const res = await server.post("clearchat", data)
        return res
    }
    return {
        clearChat
    }
})

export const useRepeatChatServer = defineStore("RepeatChatServer", () => {
    const server = axios.create({
        baseURL: SERVER_CONFIG.SERVER + ":" + SERVER_CONFIG.PORT,
        timeout: 200000,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
    })
    const repeatChat = async (data) => {
        const res = await server.post("repeatchat", data)
        return res
    }
    return {
        repeatChat
    }
})