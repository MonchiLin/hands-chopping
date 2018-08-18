import {debounceTime, map, switchMap, distinctUntilChanged, filter, publishReplay, refCount} from 'rxjs/operators'
import {Subject, merge, from,defer} from 'rxjs'

export class FetchDataStore {
    // request 是一个请求刷新数据的 API 函数,
    // 返回值为一个 Promise
    constructor(request) {
        this._subject$ = new Subject();
        this._request = request;

        // DataStore 的资源数据在首次订阅时将会获取一次，也就是说
        // 随后的每次订阅都会获得上次缓存的数据
        // 每当 refetch 调用后，data$ 将会收到新的
        this._data$ = merge(
            defer(() => this.refetch(false)),
            this._subject$.asObservable()
        ).pipe(
            publishReplay(1),
            refCount(),
            debounceTime(200),
            distinctUntilChanged(),
            switchMap(res => from(res.json()))
        )
    }

    // 返回 datastore 中的 data Observable
    get data$() {
        return this._data$;
    }

    // 重新获取新的数据。当 emit 为 true 时，
    // 发送更新事件到 data Observable
    refetch(emit = true) {
        return this._request().then(data => {
            emit && this._subject$.next(data);
            return data;
        });
    }
}