
var pos = 0;

function drawsome(){
  var c = document.getElementById("canvas");
  var ctx = c.getContext("2d");
    ctx.clearRect(0, 0, c.width, c.height);
    dis = 3.5 + Math.sin(2+pos/5)*3;
    rot = pos + Math.cos(pos/2);

    dis2 = 3.5 + Math.sin(5+pos)*3;
    rot2 = pos/2 + Math.cos(5+pos)*4;

    ctx.beginPath();
    ctx.arc(100, 200+Math.cos(5+pos)*20, 30, rot2, rot2+dis2);    
    ctx.lineWidth = 5;
    ctx.strokeStyle = "rgb(255,130,0)";
    ctx.fillStyle = "rgb(150,50,50)";
    ctx.fill();
    ctx.closePath();
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(100, 100, 70, rot, rot+dis);
    ctx.lineWidth = 10;
    ctx.strokeStyle = "rgb(25, 90,180)";
    ctx.fillStyle = "rgb(50,190,170)";
    ctx.fill();
    ctx.closePath();
    ctx.stroke();



}

function animate() {
    window.requestAnimationFrame(animate);
//    ctx.save();
    drawsome();
//    ctx.restore();
    pos += 0.03;
    console.log("animation");
}

animate();