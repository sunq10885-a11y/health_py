# react

## React Hook

1. **useState** 用于保存组件状态。`const [name, setName] = useState('')`
2. **useLayoutEffect** DOM渲染完成后立即执行，页面绘制前执行，使用场景：获取元素尺寸、滚动定位、动画计算。

```
    render
    ↓
    DOM创建完成
    ↓
    useLayoutEffect
    ↓
    浏览器绘制页面
    ↓
    useEffect
```

3. **useEffect** 处理副作用。例如：请求接口、监听事件、定时器、操作DOM,类似于vue的mounted/watch
   （1）页面加载时执行一次

```ts
useEffect(() => {
  console.log('页面加载')
}, [])
```

(2)监听变量变化

```ts
useEffect(() => {
  console.log('count变化')
}, [count])
```

（3）销毁时执行

```ts
useEffect(() => {
  console.log('组件创建')
  const timer = setInterval(() => {}, 1000)

  return () => {
    console.log('组件销毁')
    clearInterval(timer)
  }
}, [])
```

4. **useMemo**缓存计算结果 避免重复计算。相当于vue的computed,使用场景：筛选列表、排序、统计总价、树结构转换

```ts
const total = useMemo(() => {
  return list.reduce((sum, item) => sum + item.price, 0)
}, [list])
```

5. **useCallback** 缓存函数、避免函数重复创建。

```ts
const handleClick = useCallback(() => {
  console.log('click')
}, [])
```

6. **useRef** 保存引用。两个作用：获取 DOM、保存变量

```ts
const inputRef = useRef<HTMLInputElement>(null)

<input ref={inputRef} />

// 调用
inputRef.current?.focus()
```

7. **useContext** 跨组件传值

```ts
// 创建 Context：
import { createContext } from 'react'

const UserContext = createContext('')

// 提供数据
<UserContext.Provider value="Tom">
  <Child />
</UserContext.Provider>

// 获取数据
const name = useContext(UserContext)
```

8. **useReducer** 复杂状态管理 类似 Redux，使用场景购物车、表单、复杂业务状态

```ts
const reducer = (state, action) => {
  switch (action.type) {
    case 'add':
      return {
        count: state.count + 1,
      }

    default:
      return state
  }
}

// 使用
const [state, dispatch] = useReducer(reducer, { count: 0 })

// 获取数据
dispatch({
  type: 'add',
})
```

## react里面 如果请求了一个数据列表接口 后面我又变化他 但是发现dom没有更新 这个如何处理

```ts
const [list, setList] = useState<HealthRecord[]>([])

// ❌ 错误1：直接push，原数组被改了，但引用没变
const addItem = (newItem: HealthRecord) => {
  list.push(newItem)
  setList(list) // 传的还是同一个引用，React认为没变化，不重渲染！
}

// ❌ 错误2：直接改某一项的属性
const updateItem = (id: number, newDesc: string) => {
  const item = list.find((i) => i.id === id)
  if (item) {
    item.description = newDesc // 直接改了对象属性，原数组里的引用没变
  }
  setList(list) // 同样的问题
}

// ❌ 错误3：直接splice删除
const removeItem = (id: number) => {
  const index = list.findIndex((i) => i.id === id)
  list.splice(index, 1) // mutate了原数组
  setList(list)
}

// ✅ 新增：用展开运算符创建新数组
const addItem = (newItem: HealthRecord) => {
  setList([...list, newItem]);
};

// ✅ 更新某一项：用map创建新数组，里面是新对象
const updateItem = (id: number, newDesc: string) => {
  setList(list.map((item) => 
    item.id === id ? { ...item, description: newDesc } : item
  ));
};

// ✅ 删除：用filter创建新数组
const removeItem = (id: number) => {
  setList(list.filter((item) => item.id !== id));
};
```
