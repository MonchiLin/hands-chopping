import axios from 'axios'

const baseUrl = 'http://127.0.0.1:5000/'

/**
 * 获取游戏
 * @param page
 * @param per_page
 * @returns {AxiosPromise<any>}
 */
export function getGames(page, per_page) {
    const url = 'games'
    return axios.post(baseUrl + url, {
        params: {page, per_page}
    })

}

