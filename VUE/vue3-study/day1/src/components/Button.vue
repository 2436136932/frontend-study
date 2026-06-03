<script setup>
</script>

<template>
    <div class="Button">
        <button>按钮组件</button>
    </div>
</template>

<style scoped>
.Button {
    display: inline-block;
    width: 120px;
    height: 50px;
    line-height: 50px;
    padding: 0 20px;
    background-color: #3bae56;
    border-radius: 5px;
    color: white;
    border: none;
    vertical-align: middle;
    cursor: pointer;
    font-size: 16px;
}

.Button button {
    background: transparent;
    border: none;
    color: inherit;
    cursor: pointer;
    font-size: inherit;
    padding: 0;
}
</style>
