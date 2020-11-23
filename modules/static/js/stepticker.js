var time = 0;
var sinval = 0;
var rising = true;

var direction = 6;

var task_num = 0;
var timerange = [50, 20, 50, 30, 50, 20, 50, 30, 1]
var endtime = 0;
timerange[0] = timerange[0] -1

tlen = timerange.length;
for (i=0; i< tlen; i++){
    endtime += timerange[0];
    timerange.shift();
    timerange.push(endtime);
};

// console.log(timerange);

// Walker
var cx = 5;
var cy = cx;
var dx = 25;
var dy = dx;
var step = 2;
var rot = 0;
var randomrgb = [Math.random()*255,Math.random()*255,Math.random()*255]

var clockx = 50*step/2+cx+dx/2;
var clocky =  clockx;
var clockrad = 50*step/2 - dx/2-10;

var c = document.getElementById("canvas");
var ctx = c.getContext("2d");


function drawsome(){
  ctx.clearRect(0,0, c.height,c.width);
  sinval = Math.sin(time);
  if (task_num==0){cy += step;}
  else if(task_num==1){dy +=2;}
  else if(task_num==2){cx += step;}

  else if(task_num==3){dx += 2;}
  else if(task_num==4){cy -= step;}
  else if(task_num==5){dy -=2;}

  else if(task_num==6){cx -= step;}
  else if(task_num==7){dx -= 2;}
  else if(task_num==8){randomrgb=[Math.random()*255,Math.random()*255,Math.random()*255]}
  else {}

    ctx.fillStyle = "rgb("
      +((endtime-Math.abs(endtime-2*time))/endtime*randomrgb[0])+","
      +((endtime-Math.abs(endtime-2*time))/endtime*randomrgb[1])+","
      +((endtime-Math.abs(endtime-2*time))/endtime*randomrgb[2])+")"
    ctx.fillRect(cx, cy, dx, dy);


}

function tick_time(){
  for (i=0; i< timerange.length; i++){
      if (timerange[i] == time){
        task_num = (i+1) % (timerange.length);
        break;
      };
  };
}

function animate() {
    window.requestAnimationFrame(animate);
    drawsome();

    tick_time();
    time = (time+1) % (endtime+1);
}

animate();
