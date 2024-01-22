<!-- src/views/Layout/LayoutFooter/index.vue -->
<script setup>
</script>
<template>
    <footer>
        <div class="footer-content">
            <div class="copyright">2023 © dddppp</div>

            <div class="email">dddppp@outlook.com</div>
        </div>
    </footer>
</template>
    
<script>
export default {
    data() {
        return {
            showEmail: false
        }
    },
    methods: {
        toggleEmail() {
            this.showEmail = !this.showEmail;
        }
    }
}
</script>
    
<style scoped>
footer {
    position: fixed;
    z-index: 999;
    bottom: 0;
    left: 0;
    right: 0;
    background: #34495e;
    color: #fff;
    padding: 20px;
}

.footer-content {
    display: flex;
    justify-content: space-between;
    flex-direction: column;
    align-items: center;
}

.copyright {
  margin-bottom: 10px; 
}
.email {
    font-size: 14px;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}
</style>