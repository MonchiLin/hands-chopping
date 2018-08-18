import axios from 'axios'

const baseUrl = 'http://127.0.0.1:5000/'

/**
 * 获取游戏
 * @param page
 * @param per_page
 * @returns {AxiosPromise<any>}
 */
export function getGames(page = 1, per_page = 50) {
    const url = 'games'
    return axios.get(baseUrl + url, {
        params: {
            page: page,
            per_page: per_page
        }
    })

}

