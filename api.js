const API_BASE = "/api/v1"

async function apiGet(url){

    const res = await fetch(API_BASE + url)

    return await res.json()

}