<script setup>
  import axios from "axios";

  const open = async () => {
    const inp = document.getElementById('title').value;

    let data = new FormData();
    data.append('title', inp);
	data.append('token', localStorage['token']);

    await axios
        .post(`http://localhost:5001/api/get_mosaic`, data)
        .catch((err) => {
          console.log(err)
        })
        .then(async (res) => {
          const tiles = res.data.tiles
          const canvas = document.getElementById("canvas");
          const ctx = canvas.getContext("2d");

          const p = 10
          let maxX = 0;
          let maxY = 0;
          tiles.forEach(({x,y}) => {
            if(x > maxX) maxX = x;
            if(y > maxY) maxY = y;
          })

          canvas.width = maxX*p;
          canvas.height = maxY*p;
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          tiles.forEach(({x,y,r,g,b}) => {
            ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
            ctx.fillRect(x*p, y*p, p, p);
          })


        })
  }
</script>

<template>
  <div class="container">
    <input id="title" placeholder="Введите название файла">
    <button @click="open()">Open</button>
    <div class="canvas-container"><canvas id="canvas"></canvas></div>
  </div>
</template>

<style scoped>
  .container{
    height: 80%;
    width: 80%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;
    border: 2px solid black;
    border-radius: 10px;
    padding: 20px 40px;
    display: flex;
    flex-direction: column;
    gap: 20px
  }
  .canvas-container{
    margin: 30px 0 0;
    max-width: 100%;
    max-height: 400px;
    overflow: auto;
    display: flex;
    justify-content: space-around;
  }

  canvas{
    border: 6px solid black;
  }
</style>
