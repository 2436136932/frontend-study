'use strict';
const db = uniCloud.database()
const collection = db.collection('danmaku')

exports.main = async (event, context) => {
  let params = event
  if (event.body) {
    try { params = JSON.parse(event.body) } catch (e) { return { errCode: -1, errMsg: '参数解析失败' } }
  }
  const { action, nick, text, color } = params

  // 发送弹幕（发送后直接返回最新列表，省一次请求）
  if (action === 'send') {
    if (!text || text.trim().length === 0) return { errCode: -1, errMsg: '弹幕不能为空' }
    if (text.length > 20) return { errCode: -1, errMsg: '弹幕不能超过20字' }

    const item = { nick: nick || '匿名用户', text: text.trim(), color: color || '#34d399', time: Date.now() }
    await collection.add(item)

    // 超过50条删除最早的
    const countRes = await collection.count()
    if (countRes.total > 50) {
      const oldest = await collection.orderBy('time', 'asc').limit(countRes.total - 50).get()
      if (oldest.data.length > 0) {
        await collection.where({ _id: db.command.in(oldest.data.map(d => d._id)) }).remove()
      }
    }

    // 直接返回最新列表，前端不用再请求一次
    const list = await collection.orderBy('time', 'desc').limit(50).get()
    return { errCode: 0, data: list.data.reverse(), sent: item }
  }

  // 获取弹幕列表
  if (action === 'getList') {
    const res = await collection.orderBy('time', 'desc').limit(50).get()
    return { errCode: 0, data: res.data.reverse() }
  }

  // 清空弹幕
  if (action === 'clear') {
    await collection.where({ _id: db.command.exists(true) }).remove()
    return { errCode: 0, errMsg: '已清空' }
  }

  return { errCode: -1, errMsg: '未知操作' }
}
