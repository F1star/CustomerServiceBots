import { defineStore } from "pinia";
import { SERVER_CONFIG } from "../../config";
import axios from "axios";

export const useGetInfoServer = defineStore("GetInfoServer", () => {
    const server = axios.create({
        baseURL: SERVER_CONFIG.SERVER + ":" + SERVER_CONFIG.PORT,
        timeout: 100000,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
    })
    const getInfo = async (data) => {
        const res = await server.post("getinfo", data)
        return res
    }
    return {
        getInfo
    }
})

export const useSetInfoServer = defineStore("SetInfoServer", () => {
    const server = axios.create({
        baseURL: SERVER_CONFIG.SERVER + ":" + SERVER_CONFIG.PORT,
        timeout: 20000,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
    })
    const setInfo = async (data) => {
        const res = await server.post("setinfo", data)
        return res
    }
    return {
        setInfo
    }
})