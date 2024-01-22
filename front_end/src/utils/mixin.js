// /src/utils/mixin.js
// 屏幕适配 mixin 函数
const scale = {
    width: '1',
    height: '1',
  }
  
  const baseWidth = 1920
  const baseHeight = 1080
  const baseProportion = parseFloat((baseWidth / baseHeight).toFixed(5))
  
  export default {
    data() {
      return {
        drawTiming: null
      }
    },
    mounted () {
      this.calcRate()
      window.addEventListener('resize', this.resize)
    },
    beforeDestroy () {
      window.removeEventListener('resize', this.resize)
    },
    methods: {
      calcRate () {
        const appRef = this.$refs["zoom"]
        if (!appRef) return 
        const currentRate = parseFloat((window.innerWidth / window.innerHeight).toFixed(5))
        if (appRef) {
          if (currentRate > baseProportion) {
            scale.width = ((window.innerHeight * baseProportion) / baseWidth).toFixed(5)
            scale.height = (window.innerHeight / baseHeight).toFixed(5)
            appRef.style.transform = `scale(${scale.width}, ${scale.height}) translate(-50%, -50%)`
          } else {
            scale.height = ((window.innerWidth / baseProportion) / baseHeight).toFixed(5)
            scale.width = (window.innerWidth / baseWidth).toFixed(5)
            appRef.style.transform = `scale(${scale.width}, ${scale.height}) translate(-50%, -50%)`
          }
        }
      },
      resize () {
        //先清除计时器
        clearTimeout(this.drawTiming)
        //开启计时器
        this.drawTiming = setTimeout(() => {
          this.calcRate()
        }, 200)
      }
    },
  }
  