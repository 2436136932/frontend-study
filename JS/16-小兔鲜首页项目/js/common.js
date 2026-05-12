// 获取电梯导航容器
const elevator = document.querySelector('.elevator');
// 获取电梯导航的 ul 列表
const elevatorUl = document.querySelector('.elevator-ul');
// 给 ul 绑定点击事件（事件委托）
elevatorUl.addEventListener('click', function (e) {
    // 判断点击的是否为 a 标签
    if (e.target.tagName === 'A') {
        // 排他思想：先移除旧的 active，再给当前元素添加 active
        // 1. 查找当前已有 active 类的元素
        const old = document.querySelector('.active');
        // 2. 如果存在，移除它的 active 类
        if (old) {
            old.classList.remove('active');
        }
        // 3. 给当前点击的 a 标签添加 active 类
        if (e.target.dataset.name === 'back-top') {
            e.target.classList.remove('active');
        } else {
            e.target.classList.add('active');
        }

        // 4. 获取点击的 a 标签的 data-name 属性值
        // console.log(document.querySelector(`#${e.target.dataset.name}`).offsetTop);
        const top = document.querySelector(`#${e.target.dataset.name}`).offsetTop;
        // 5. 根据 name 值，滚动到对应模块
        document.documentElement.scrollTop = top;
        
    }
})

const entry = document.querySelector('.entry');
window.addEventListener('scroll', function () {
    const windowScrollY = document.documentElement.scrollTop;
    // if (windowScrollY >= entry.offsetTop) {
    //     elevator.style.opacity = 1;
    // } else {
    //     elevator.style.opacity = 0;
    // }
    elevator.style.opacity = windowScrollY >= entry.offsetTop ? 1 : 0;
})
