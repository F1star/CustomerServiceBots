import { defineStore } from "pinia";
import { useLoginServer } from "./server";

export const useUserStore = defineStore("user", () => {
    const server = useLoginServer();

    async function login(user) {
        const res = await server.login(user);
        return res;
    }

    async function register(user) {
        const res = await server.register(user);
        return res;
    }

    return {
        login,
        register
    };
});
