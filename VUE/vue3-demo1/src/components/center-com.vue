<script setup>
import BottomCom from './bottom-com.vue'
// ====== 中间层组件 ======
// 不需要 provide / inject 任何东西
// provide 的数据会**自动穿透**中间层，直达底层
</script>

<template>
    <div class="center">
        <h2>我是中间层组件</h2>
    </div>
    <!-- 引入底层组件，形成组件嵌套：App → CenterCom → BottomCom -->
    <BottomCom />
</template>

<style scoped>
.center {
    height: 100px;
    width: 100%;
    background-color: skyblue;
    margin: 0px auto;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}
</style>
