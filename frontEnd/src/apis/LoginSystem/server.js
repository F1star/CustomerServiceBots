import { defineStore } from "pinia";
import { SERVER_CONFIG } from "../../config";
import axios from "axios";

export const useLoginServer = defineStore("loginServer", () => {
    const server = axios.create({
        baseURL: `${SERVER_CONFIG.SERVER}:${SERVER_CONFIG.PORT}`,
        timeout: 10000,
        headers: {
            'Content-Type': 'multipart/form-data'
        },
    });

    const login = async (data) => {
        const res = await server.post("login", data);
        return res;
    };
    const register = async (data) => {
        const res = await server.post("register", data);
        return res;
    };

    return {
        login,
        register
    };
});
